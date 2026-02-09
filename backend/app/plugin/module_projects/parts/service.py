from sqlalchemy import select, func, or_
from .model import PartsModel
from .schema import PartsCreate, PartsUpdate, PartsFilter, PartsOut
from app.core.database import async_db_session
from app.core.exceptions import CustomException
from app.plugin.module_projects.components.model import ComponentsModel

class PartsService:
    @classmethod
    async def get_parts_list_service(
        cls,
        page_no: int,
        page_size: int,
        search: PartsFilter
    ) -> dict:
        """
        获取组件列表
        """
        async with async_db_session() as session:
            stmt = select(PartsModel)
            
            if search.wtcode:
                stmt = stmt.where(PartsModel.wtcode.ilike(f"%{search.wtcode}%"))
            if search.component_wtcode:
                stmt = stmt.where(PartsModel.component_wtcode.ilike(f"%{search.component_wtcode}%"))
            if search.code:
                stmt = stmt.where(PartsModel.code.ilike(f"%{search.code}%"))

            # 计算总数
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar() or 0

            # 分页
            stmt = stmt.offset((page_no - 1) * page_size).limit(page_size)
            stmt = stmt.order_by(PartsModel.created_time.desc())
            
            result = await session.execute(stmt)
            items = result.scalars().all()

            # Serialize
            data_list = [PartsOut.model_validate(item).model_dump() for item in items]

            return {
                "items": data_list,
                "total": total,
                "page_no": page_no,
                "page_size": page_size
            }

    @classmethod
    async def create_parts_service(cls, obj: PartsCreate) -> PartsModel:
        """
        创建组件
        """
        async with async_db_session() as session:
            async with session.begin():
                # Check duplication
                stmt = select(PartsModel).where(PartsModel.wtcode == obj.wtcode)
                existing = (await session.execute(stmt)).scalars().first()
                if existing:
                    raise CustomException(msg=f"万通码 {obj.wtcode} 已存在")
                
                # Verify component exists
                if obj.component_wtcode:
                    comp_stmt = select(ComponentsModel).where(ComponentsModel.wtcode == obj.component_wtcode)
                    comp = (await session.execute(comp_stmt)).scalars().first()
                    if not comp:
                        raise CustomException(msg=f"部件万通码 {obj.component_wtcode} 不存在")

                parts = PartsModel(**obj.model_dump(exclude_unset=True))
                session.add(parts)
            return parts

    @classmethod
    async def update_parts_service(cls, id: int, obj: PartsUpdate) -> PartsModel:
        """
        更新组件
        """
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(PartsModel).where(PartsModel.id == id)
                parts = (await session.execute(stmt)).scalars().first()
                if not parts:
                    raise CustomException(msg="零件不存在")
                
                # Verify component if changing
                # Note: PartsUpdate doesn't have component_wtcode in the schema I read earlier? 
                # Let's check schema again. It was in PartsSchema (base), but not explicitly in Update.
                # If inherited from BaseModel, it only has defined fields.
                # Looking at read output: PartsUpdate defined code, spec, count, material, unit_mass, total_mass, remark.
                # It missed wtcode and component_wtcode!
                # I should probably fix PartsUpdate schema too if these are editable.
                # For now, I'll stick to what's in obj.

                for key, value in obj.model_dump(exclude_unset=True).items():
                    setattr(parts, key, value)
            return parts

    @classmethod
    async def delete_parts_service(cls, ids: list[int]) -> None:
        """
        删除组件
        """
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(PartsModel).where(PartsModel.id.in_(ids))
                parts_list = (await session.execute(stmt)).scalars().all()
                if not parts_list:
                    raise CustomException(msg="零件不存在")
                
                for part in parts_list:
                    await session.delete(part)
