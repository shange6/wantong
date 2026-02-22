from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from .service import PartsService
from .schema import PartsCreate, PartsUpdate, PartsFilter, PartsOut
from app.core.router_class import OperationLogRoute
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission

PartsRouter = APIRouter(route_class=OperationLogRoute, prefix="/parts", tags=["项目管理"])

@PartsRouter.get("/list", summary="获取组件列表")
async def get_parts_list(
    # page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PartsFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:parts:query"]))]
):
    data = await PartsService.get_parts_list_service(
        # page_no=page.page_no,
        # page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@PartsRouter.post("/create", summary="创建组件")
async def create_parts(
    obj: PartsCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:parts:create"]))]
):
    data = await PartsService.create_parts_service(obj)
    return SuccessResponse(data=data)

@PartsRouter.put("/update/{id}", summary="更新组件")
async def update_parts(
    id: int, 
    obj: PartsUpdate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:parts:update"]))]
):
    data = await PartsService.update_parts_service(id, obj)
    return SuccessResponse(data=data)

@PartsRouter.delete("/delete", summary="删除组件")
async def delete_parts(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_projects:parts:delete"]))]
):
    await PartsService.delete_parts_service(ids)
    return SuccessResponse(msg="Deleted successfully")
