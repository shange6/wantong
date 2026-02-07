import os
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from .schema import DataUploadSchema
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

            return DataUploadSchema(
                filename=filename,
                file_url=file_url,
                file_size=len(content),
                upload_time=datetime.now(),
            ).model_dump(mode="json")

        except Exception as e:
            log.error(f"文件上传失败: {e!s}")
            raise CustomException(msg=f"文件上传失败: {e!s}")

