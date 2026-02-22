import os
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.core.database import async_db_session
from sqlalchemy import select
from app.plugin.module_projects.projects.model import ProjectsModel
from app.plugin.module_projects.components.model import ComponentsModel
from app.plugin.module_projects.parts.model import PartsModel
from .schema import DatasUploadSchema, SaveDatasSchema
from .dwg2dict import dwg2dxf, dxf2dict
from .list2tree import list2tree
from .wtdata import getwtcode

class DatasService:
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
    async def save_datas_service(cls, payload: SaveDatasSchema) -> dict:
        """
        保存订单数据：先验证是否存在，不存在则插入
        """
        # 初始化统计数据
        stats = {"project_added": 0, "component_added": 0, "parts_added": 0}
        async with async_db_session() as session:
            async with session.begin():
                # 1. 处理项目信息 (根据 no 或 code 判断唯一性)
                project_stmt = select(ProjectsModel).where(
                    (ProjectsModel.no == payload.projects.no) | 
                    (ProjectsModel.code == payload.projects.code)
                )
                project_result = await session.execute(project_stmt)
                project = project_result.scalars().first()

                if not project:
                    project = ProjectsModel(
                        name=payload.projects.name,
                        code=payload.projects.code,
                        no=payload.projects.no,
                    )
                    session.add(project)
                    # 必须 flush 以确保后续组件能拿到 project_id 或正确的 code 关联
                    await session.flush()
                    stats["projects_added"] = 1  # 记录新增项目
                else:
                    # 如果项目已存在，直接使用查询到的对象，不进行任何修改
                    pass

                # 2. 处理组件信息 (根据 wtcode 判断唯一性)
                component_stmt = select(ComponentsModel).where(
                    ComponentsModel.wtcode == payload.components.wtcode
                )
                comp_result = await session.execute(component_stmt)
                component = comp_result.scalars().first()

                if not component:
                    component = ComponentsModel(
                        # project_id=project.id,  # 建议使用 ID 关联更稳定
                        project_code=project.code,
                        # parent_code=payload.components.parent_code, # Aliased field
                        wtcode=payload.components.wtcode,
                        spec=payload.components.spec,
                        code=payload.components.code,
                        count=payload.components.count,
                        material=payload.components.material,
                        unit_mass=payload.components.unit_mass,
                        total_mass=payload.components.total_mass,
                        remark=payload.components.remark,
                    )
                    session.add(component)
                    await session.flush()
                    stats["components_added"] = 1  # 记录新增组件

                # 3. 处理明细信息 (Parts)
                # 假设 parts 数量较多，先一次性查询出该组件下已存在的 wtcode
                existing_parts_stmt = select(PartsModel.wtcode).where(
                    PartsModel.component_wtcode == (component.wtcode if hasattr(component, 'wtcode') else None)
                )
                existing_parts_result = await session.execute(existing_parts_stmt)
                existing_wtcodes = set(existing_parts_result.scalars().all())

                for item in payload.parts:
                    # 如果当前 wtcode 不在数据库中，则插入
                    if item.wtcode not in existing_wtcodes:
                        detail = PartsModel(
                            # component_id=component.id, # 确保外键关联
                            component_wtcode=component.wtcode,
                            wtcode=item.wtcode,
                            code=item.code,
                            spec=item.spec,

                            count=item.count,
                            material=item.material,
                            unit_mass=item.unit_mass,
                            total_mass=item.total_mass,
                            remark=item.remark,
                        )
                        session.add(detail)
                        stats["parts_added"] += 1  # 累加新增明细数量
        # 5. 返回统计结果（你可以根据需要打印/记录日志/返回给前端）
        return stats
