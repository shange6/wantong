from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, UploadFile, Body
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import DataService
from .schema import SaveDataSchema

# 注意：prefix 设为 /data，因为 module_orders 会自动生成 /orders 前缀
# 最终路径将是 /api/v1/orders/data/upload
DataRouter = APIRouter(route_class=OperationLogRoute, prefix="/data", tags=["订单数据"])

@DataRouter.post(
    "/upload",
    summary="上传订单数据",
    description="上传文件到指定目录",
)
async def upload_file_controller(
    file: UploadFile,
    request: Request,
    target_path: Annotated[str | None, Form(description="目标目录路径")] = None,
) -> JSONResponse:
    """
    上传文件
    """
    result_dict = await DataService.upload_file_service(
        file=file, target_path=target_path, base_url=str(request.base_url)
    )
    # log.info(f"上传文件成功: {result_dict['filename']}")
    return SuccessResponse(data=result_dict, msg="上传文件成功")

@DataRouter.post(
    "/savedata",
    summary="保存订单数据",
    description="保存解析后的数据到数据库",
)
async def save_data_controller(
    payload: SaveDataSchema
) -> JSONResponse:
    """
    保存前端数据到数据库
    """
    # 这里暂时只打印日志，后续可以调用 Service 层进行入库操作
    print("222222222222222222222222222222222222222")
    log.info(f"接收到保存数据请求，{payload}, 明细条数: {len(payload.details)}")
    
    # 模拟保存成功
    return SuccessResponse(msg="保存数据成功")
