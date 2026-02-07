from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, Query, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from app.common.request import PaginationService
from app.common.response import StreamResponse, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute
from app.utils.common_util import bytes2file_response

# from .schema import (
#     ResourceCopySchema,
#     ResourceCreateDirSchema,
#     ResourceMoveSchema,
#     ResourceRenameSchema,
#     ResourceSearchQueryParam,
# )
from .service import ResourceService

DataRouter = APIRouter(route_class=OperationLogRoute, prefix="/data", tags=["导入数据"])
# DemoRouter = APIRouter(route_class=OperationLogRoute, prefix="/demo", tags=["示例模块"])


@FileRouter.post(
    "/upload",
    summary="上传文件",
    description="上传文件",
    dependencies=[Depends(AuthPermission(["module_common:file:upload"]))],
)
async def upload_controller(
    file: UploadFile,
    request: Request,
) -> JSONResponse:
    """
    上传文件

    参数:
    - file (UploadFile): 上传的文件
    - request (Request): 请求对象

    返回:
    - JSONResponse: 包含上传文件详情的JSON响应
    """
    result_dict = await FileService.upload_service(base_url=str(request.base_url), file=file)
    log.info(f"上传文件成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="上传文件成功")


