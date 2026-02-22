from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, UploadFile, Body
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .service import DatasService
from .schema import SaveDatasSchema

# 注意：prefix 设为 /datas，因为 module_projects 会自动生成 /projects 前缀
# 最终路径将是 /api/v1/projects/datas/upload
DatasRouter = APIRouter(route_class=OperationLogRoute, prefix="/datas", tags=["项目管理"])

@DatasRouter.post(
    "/upload",
    summary="上传数据文件",
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
    result_dict = await DatasService.upload_file_service(
        file=file, target_path=target_path, base_url=str(request.base_url)
    )
    # log.info(f"上传文件成功: {result_dict['filename']}")
    return SuccessResponse(data=result_dict, msg="上传文件成功")

@DatasRouter.post(
    "/savedatas",
    summary="保存项目信息",
    description="保存解析后的数据到数据库",
)
async def save_data_controller(
    payload: SaveDatasSchema
) -> JSONResponse:
    """
    保存前端数据到数据库
    """
    result =await DatasService.save_datas_service(payload)
    msg = f"保存数据成功! 新增项目: {result.get('projects_added')}, 新增部件: {result.get('components_added')}, 新增零件: {result.get('parts_added')}"
    log.info(msg)
    return SuccessResponse(data=result, msg=msg)
