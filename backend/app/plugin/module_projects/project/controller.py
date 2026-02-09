from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission
from .service import ProjectService
from .schema import ProjectCreate, ProjectUpdate, ProjectFilter

ProjectRouter = APIRouter(prefix="/project", tags=["项目管理"])

@ProjectRouter.get("/list", summary="获取项目列表")
async def get_project_list(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ProjectFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:query"]))]
):
    data = await ProjectService.get_project_list_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@ProjectRouter.post("/create", summary="创建项目")
async def create_project(
    data: ProjectCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:create"]))]
):
    result = await ProjectService.create_project_service(data)
    return SuccessResponse(msg="创建成功")

@ProjectRouter.put("/update/{id}", summary="更新项目")
async def update_project(
    id: int,
    data: ProjectUpdate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:update"]))]
):
    await ProjectService.update_project_service(id, data)
    return SuccessResponse(msg="更新成功")

@ProjectRouter.delete("/delete", summary="删除项目")
async def delete_project(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:project:delete"]))]
):
    await ProjectService.delete_project_service(ids)
    return SuccessResponse(msg="删除成功")
