from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from .service import OrdersService
from .schema import OrdersCreate, OrdersUpdate, OrdersFilter, OrdersOut, OrdersCreateOut
from app.core.router_class import OperationLogRoute
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission

OrdersRouter = APIRouter(route_class=OperationLogRoute, prefix="/order", tags=["工单管理"])

@OrdersRouter.get("/uncreatelist", summary="获取待创建工单列表")
async def get_uncreate_list(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[OrdersFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:query"]))]
):
    data = await OrdersService.get_uncreate_list_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@OrdersRouter.get("/unlaborhourlist", summary="获取待填写工时列表")
async def get_unlaborhour_list(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[OrdersFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:query"]))]
):
    data = await OrdersService.get_unlaborhour_list_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@OrdersRouter.get("/list", summary="获取工单列表")
async def get_orders_list(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[OrdersFilter, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:query"]))]
):
    data = await OrdersService.get_orders_list_service(
        page_no=page.page_no,
        page_size=page.page_size,
        search=search
    )
    return SuccessResponse(data=data)

@OrdersRouter.post("/create", summary="创建工单", response_model=OrdersCreateOut)
async def create_orders(
    obj: OrdersCreate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:create"]))]
):
    data = await OrdersService.create_orders_service(obj)
    return SuccessResponse(data=jsonable_encoder(data))

@OrdersRouter.put("/update/{id}", summary="更新工单")
async def update_orders(
    id: int, 
    obj: OrdersUpdate,
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:update"]))]
):
    data = await OrdersService.update_orders_service(id, obj)       
    return SuccessResponse(data=jsonable_encoder(OrdersOut.model_validate(data)))

@OrdersRouter.delete("/delete", summary="删除工单")
async def delete_orders(
    ids: list[int],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_orders:order:delete"]))] 
):
    await OrdersService.delete_orders_service(ids)
    return SuccessResponse(msg="删除成功")
