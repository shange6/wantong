from sqlalchemy import select, func, or_
from .model import ComponentsModel
from app.plugin.module_projects.project.model import ProjectsModel
from .schema import ComponentsCreate, ComponentsUpdate, ComponentsFilter, ComponentsOut
from app.core.database import async_db_session
from app.core.exceptions import CustomException

class ComponentsService:
    @classmethod
    async def get_components_list_service(cls, page_no: int, page_size: int, search: ComponentsFilter):
        async with async_db_session() as session:
            stmt = select(ComponentsModel)
            
            # Filters
            if search.project_code:
                stmt = stmt.where(ComponentsModel.project_code.ilike(f"%{search.project_code}%"))
            if search.wtcode:
                stmt = stmt.where(ComponentsModel.wtcode.ilike(f"%{search.wtcode}%"))
            if search.code:
                stmt = stmt.where(ComponentsModel.code.ilike(f"%{search.code}%"))
            if search.name:
                stmt = stmt.where(ComponentsModel.name.ilike(f"%{search.name}%"))
            
            # Total count
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar() or 0
            
            # Pagination
            stmt = stmt.offset((page_no - 1) * page_size).limit(page_size)
            stmt = stmt.order_by(ComponentsModel.created_time.desc())
            
            result = await session.execute(stmt)
            items = result.scalars().all()
            
            # Serialize to Pydantic models then to dicts
            data_list = [ComponentsOut.model_validate(item).model_dump() for item in items]
            
            return {
                "items": data_list,
                "total": total,
                "page_no": page_no,
                "page_size": page_size
            }

    @classmethod
    async def create_components_service(cls, data: ComponentsCreate):
        async with async_db_session() as session:
            async with session.begin():
                # Check duplication
                stmt = select(ComponentsModel).where(ComponentsModel.wtcode == data.wtcode)
                existing = (await session.execute(stmt)).scalars().first()
                if existing:
                     raise CustomException(msg=f"万通编码 {data.wtcode} 已存在")
                
                # Verify project exists
                project_stmt = select(ProjectsModel).where(ProjectsModel.code == data.project_code)
                project = (await session.execute(project_stmt)).scalars().first()
                if not project:
                     raise CustomException(msg=f"项目编号 {data.project_code} 不存在")

                component = ComponentsModel(**data.model_dump(exclude_unset=True))
                session.add(component)
            return component

    @classmethod
    async def update_components_service(cls, id: int, data: ComponentsUpdate):
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(ComponentsModel).where(ComponentsModel.id == id)
                component = (await session.execute(stmt)).scalars().first()
                if not component:
                    raise CustomException(msg="部件不存在")
                
                # Check duplication if modifying wtcode
                if data.wtcode and data.wtcode != component.wtcode:
                    existing = (await session.execute(select(ComponentsModel).where(ComponentsModel.wtcode == data.wtcode))).scalars().first()
                    if existing:
                        raise CustomException(msg=f"万通编码 {data.wtcode} 已存在")
                
                # Verify project if modifying project_code
                if data.project_code and data.project_code != component.project_code:
                    project = (await session.execute(select(ProjectsModel).where(ProjectsModel.code == data.project_code))).scalars().first()
                    if not project:
                        raise CustomException(msg=f"项目编号 {data.project_code} 不存在")

                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(component, key, value)
            return component

    @classmethod
    async def delete_components_service(cls, ids: list[int]):
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(ComponentsModel).where(ComponentsModel.id.in_(ids))
                components = (await session.execute(stmt)).scalars().all()
                if not components:
                     raise CustomException(msg="部件不存在")
                
                for component in components:
                    await session.delete(component)
