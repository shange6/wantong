from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission
from .service import ComponentsService
from .schema import ComponentsCreate, ComponentsUpdate, ComponentsFilter

ComponentsRouter = APIRouter(prefix="/components", tags=["部件管理"])

@ComponentsRouter.get("/list", summary="获取部件列表")
async def get_components_list(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[ComponentsFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:components:query"]))]
):
    data = await ComponentsService.get_components_list_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@ComponentsRouter.post("/create", summary="创建部件")
async def create_components(
    data: ComponentsCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:components:create"]))]
):
    await ComponentsService.create_components_service(data)
    return SuccessResponse(msg="创建成功")

@ComponentsRouter.put("/update/{id}", summary="更新部件")
async def update_components(
    id: int,
    data: ComponentsUpdate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:components:update"]))]
):
    await ComponentsService.update_components_service(id, data)
    return SuccessResponse(msg="更新成功")

@ComponentsRouter.delete("/delete", summary="删除部件")
async def delete_components(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:components:delete"]))]
):
    await ComponentsService.delete_components_service(ids)
    return SuccessResponse(msg="删除成功")
