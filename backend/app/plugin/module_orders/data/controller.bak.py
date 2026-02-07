from typing import Annotated

from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import DataService

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
