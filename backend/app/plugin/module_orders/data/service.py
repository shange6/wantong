import os
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.database import async_db_session
from .schema import DataUploadSchema, SaveDataSchema
from .model import OrderProjectModel, OrderComponentModel, OrderDetailModel
from .dwg2dict import dwg2dxf, dxf2dict
from .wtdata import getwtcode
from .list2tree import list2tree

class DataService:
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB

    @classmethod
    async def upload_file_service(
        cls,
        file: UploadFile,
        target_path: str | None = None,
        base_url: str | None = None,
    ) -> dict:
        if not file or not file.filename:
            raise CustomException(msg="请选择要上传的文件")

        # 简单的安全检查
        if ".." in file.filename:
            raise CustomException(msg="文件名包含不安全字符")

        try:
            content = await file.read()
            if len(content) > cls.MAX_UPLOAD_SIZE:
                raise CustomException(msg=f"文件太大，最大支持{cls.MAX_UPLOAD_SIZE // (1024 * 1024)}MB")

            # 使用静态资源目录下的 orders/data 目录
            resource_root = str(settings.STATIC_ROOT)
            save_dir = os.path.join(resource_root)
            
            if target_path:
                # 简单的路径组合，实际生产环境需要更严格的安全检查
                # 这里为了简单，假设 target_path 是相对路径且不包含 ..
                potential_path = os.path.join(save_dir, target_path.strip("/"))
                # 确保路径在 save_dir 下
                if os.path.commonpath([os.path.abspath(potential_path), os.path.abspath(save_dir)]) == os.path.abspath(save_dir):
                     save_dir = potential_path

            os.makedirs(save_dir, exist_ok=True)

            filename = "upload_" + os.path.splitext(file.filename)[1]
            file_path = os.path.join(save_dir, filename)

            Path(file_path).write_bytes(content)

            # 生成访问 URL
            # 假设 STATIC_URL 是 /static
            relative_path = os.path.relpath(file_path, resource_root)
            url_path = relative_path.replace(os.sep, "/")
            file_url = f"{settings.STATIC_URL}/{url_path}".replace("//", "/")

            if base_url:
                 file_url = f"{base_url.rstrip('/')}{file_url}"

            return list2tree(getwtcode(dxf2dict(dwg2dxf(file_path))))

        except Exception as e:
            log.error(f"文件上传失败: {e!s}")
            raise CustomException(msg=f"文件上传失败: {e!s}")

    @classmethod
    async def save_data_service(cls, payload: SaveDataSchema) -> None:
        """
        保存订单数据
        """
        async with async_db_session() as session:
            async with session.begin():
                # 1. 保存项目信息
                # 暂时每次都创建新项目记录，或者根据 contractNo/projectCode 判断是否存在
                # 这里简单处理，每次保存都视为新的入库记录（或者同一个项目的不同批次）
                project = OrderProjectModel(
                    project_name=payload.project_info.projectName,
                    project_code=payload.project_info.projectCode,
                    contract_no=payload.project_info.contractNo,
                )
                session.add(project)
                await session.flush()  # 获取 project.id

                # 2. 保存组件信息
                component = OrderComponentModel(
                    project_id=project.id,
                    parent_code=payload.component_info.parentCode,
                    component_name=payload.component_info.componentName,
                    component_code=payload.component_info.componentCode,
                    component_count=payload.component_info.componentCount,
                )
                session.add(component)
                await session.flush()  # 获取 component.id

                # 3. 保存明细信息
                details = []
                for item in payload.details:
                    # 处理 count 可能是 str 或 int
                    count_val = str(item.count) if item.count is not None else None
                    
                    detail = OrderDetailModel(
                        component_id=component.id,
                        wtcode=item.wtcode,
                        code=item.code,
                        spec=item.spec,
                        count=count_val,
                        material=item.material,
                        unit_mass=item.unit_mass,
                        total_mass=item.total_mass,
                        remark=item.remark,
                    )
                    details.append(detail)
                
                session.add_all(details)
                # 提交事务由 async with session.begin() 自动处理
