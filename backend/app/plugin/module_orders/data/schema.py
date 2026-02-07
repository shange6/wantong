from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

class DataUploadSchema(BaseModel):
    """数据上传响应模型"""
    model_config = ConfigDict(from_attributes=True)
    filename: str = Field(..., description="文件名")
    file_url: str = Field(..., description="访问URL")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(..., description="上传时间")

class ProjectInfoSchema(BaseModel):
    projectName: Optional[str] = None
    projectCode: Optional[str] = None
    contractNo: Optional[str] = None

class ComponentInfoSchema(BaseModel):
    parentCode: Optional[str] = None
    componentName: Optional[str] = None
    componentCode: Optional[str] = None
    componentCount: Optional[int] = None

class DetailItemSchema(BaseModel):
    # id: Optional[int] = None
    # seq: Optional[str] = None
    wtcode: Optional[str] = None
    code: Optional[str] = None
    spec: Optional[str] = None
    count: Optional[Union[str, int]] = None
    material: Optional[str] = None
    unit_mass: Optional[Union[int, float]] = None
    total_mass: Optional[Union[int, float]] = None
    remark: Optional[str] = None

class SaveDataSchema(BaseModel):
    project_info: ProjectInfoSchema
    component_info: ComponentInfoSchema
    details: List[DetailItemSchema]
