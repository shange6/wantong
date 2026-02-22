from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.common.response import SuccessResponse
# from app.core.base_params import PaginationQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission
from .service import ProjectsService
from .schema import ProjectsCreate, ProjectsUpdate, ProjectsFilter

ProjectsRouter = APIRouter(prefix="/projects", tags=["项目管理"])

@ProjectsRouter.get("/list", summary="获取项目列表")
async def get_project_list(
    # page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ProjectsFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:query"]))]
):
    data = await ProjectsService.get_projects_list_service(
        # page_no=page.page_no,
        # page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@ProjectsRouter.post("/create", summary="创建项目")
async def create_project(
    data: ProjectsCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:create"]))]
):
    result = await ProjectsService.create_projects_service(data)
    return SuccessResponse(msg="创建成功")

@ProjectsRouter.put("/update/{id}", summary="更新项目")
async def update_project(
    id: int,
    data: ProjectsUpdate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:update"]))]
):
    await ProjectsService.update_projects_service(id, data)
    return SuccessResponse(msg="更新成功")

@ProjectsRouter.delete("/delete", summary="删除项目")
async def delete_project(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:delete"]))]
):
    await ProjectsService.delete_projects_service(ids)
    return SuccessResponse(msg="删除成功")
