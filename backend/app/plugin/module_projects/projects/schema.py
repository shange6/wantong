from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ProjectsBase(BaseModel):
    """
    项目基础模型
    """
    code: str
    name: str
    no: str

class ProjectsCreate(ProjectsBase):
    """
    创建项目
    """
    pass

class ProjectsUpdate(BaseModel):
    """
    更新项目
    """
    code: Optional[str] = None
    name: Optional[str] = None
    no: Optional[str] = None

class ProjectsFilter(BaseModel):
    """
    项目查询参数
    """
    code: Optional[str] = None
    name: Optional[str] = None
    no: Optional[str] = None
    
    model_config = ConfigDict(extra="ignore")

class ProjectsOut(ProjectsBase):
    """
    项目输出模型
    """
    # id: int
    # created_time: datetime
    # updated_time: datetime    
    model_config = ConfigDict(from_attributes=True)
