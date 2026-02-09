from sqlalchemy import select, func, or_
from .model import ProjectsModel
from .schema import ProjectCreate, ProjectUpdate, ProjectFilter, ProjectOut
from app.core.database import async_db_session
from app.core.exceptions import CustomException

class ProjectService:
    @classmethod
    async def get_project_list_service(cls, page_no: int, page_size: int, search: ProjectFilter):
        async with async_db_session() as session:
            stmt = select(ProjectsModel)
            
            # Filters
            if search.code:
                stmt = stmt.where(ProjectsModel.code.ilike(f"%{search.code}%"))
            if search.name:
                stmt = stmt.where(ProjectsModel.name.ilike(f"%{search.name}%"))
            if search.no:
                stmt = stmt.where(ProjectsModel.no.ilike(f"%{search.no}%"))
            
            # Total count
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar() or 0
            
            # Pagination
            stmt = stmt.offset((page_no - 1) * page_size).limit(page_size)
            stmt = stmt.order_by(ProjectsModel.code.desc())
            
            result = await session.execute(stmt)
            items = result.scalars().all()
            
            # Serialize to Pydantic models then to dicts
            data_list = [ProjectOut.model_validate(item).model_dump() for item in items]
            
            return {
                "items": data_list,
                "total": total,
                "page_no": page_no,
                "page_size": page_size
            }

    @classmethod
    async def create_project_service(cls, data: ProjectCreate):
        async with async_db_session() as session:
            async with session.begin():
                # Check duplication
                stmt = select(ProjectsModel).where(
                    or_(ProjectsModel.code == data.code, ProjectsModel.no == data.no)
                )
                existing = (await session.execute(stmt)).scalars().first()
                if existing:
                     raise CustomException(msg="项目编号或合同号已存在")
                
                project = ProjectsModel(**data.model_dump(exclude_unset=True))
                session.add(project)
            return project

    @classmethod
    async def update_project_service(cls, id: int, data: ProjectUpdate):
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(ProjectsModel).where(ProjectsModel.id == id)
                project = (await session.execute(stmt)).scalars().first()
                if not project:
                    raise CustomException(msg="项目不存在")
                
                # Check duplication if modifying code/no
                if data.code and data.code != project.code:
                    existing = (await session.execute(select(ProjectsModel).where(ProjectsModel.code == data.code))).scalars().first()
                    if existing:
                        raise CustomException(msg=f"项目编号 {data.code} 已存在")

                if data.no and data.no != project.no:
                    existing = (await session.execute(select(ProjectsModel).where(ProjectsModel.no == data.no))).scalars().first()
                    if existing:
                        raise CustomException(msg=f"合同号 {data.no} 已存在")

                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(project, key, value)
            return project

    @classmethod
    async def delete_project_service(cls, ids: list[int]):
        async with async_db_session() as session:
            async with session.begin():
                stmt = select(ProjectsModel).where(ProjectsModel.id.in_(ids))
                projects = (await session.execute(stmt)).scalars().all()
                if not projects:
                     raise CustomException(msg="项目不存在")
                
                for project in projects:
                    await session.delete(project)
