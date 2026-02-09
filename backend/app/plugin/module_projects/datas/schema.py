from typing import List, Optional
from pydantic import BaseModel, Field

from app.plugin.module_projects.project.schema import ProjectCreate
from app.plugin.module_projects.components.schema import ComponentsCreate
from app.plugin.module_projects.parts.schema import PartsCreate

class DatasUploadSchema(BaseModel):
    """数据上传响应模型"""
    filename: str = Field(..., description="文件名")
    file_url: str = Field(..., description="访问URL")
    file_size: int = Field(..., description="文件大小")
    upload_time: str = Field(..., description="上传时间") # datetime serialized

class ProjectsImportSchema(ProjectCreate):
    pass

class ComponentsImportSchema(ComponentsCreate):
    parent_code: Optional[str] = Field(None, alias="parentCode")
    # datas module expects 'parentCode' in JSON, maps to 'parent_code' in model

class PartsImportSchema(PartsCreate):
    pass

class SaveDatasSchema(BaseModel):
    projects: ProjectsImportSchema
    components: ComponentsImportSchema
    parts: List[PartsImportSchema]
