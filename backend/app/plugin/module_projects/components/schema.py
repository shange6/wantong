from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ComponentsBase(BaseModel):
    """
    部件基础模型
    """
    project_code: str
    wtcode: str
    code: str
    name: str
    count: int
    material: str
    unit_mass: float | None = None
    total_mass: float | None = None
    remark: Optional[str] = None

class ComponentsCreate(ComponentsBase):
    """
    创建部件
    """
    pass

class ComponentsUpdate(BaseModel):
    """
    更新部件
    """
    project_code: Optional[str] = None
    parent_code: Optional[str] = None
    wtcode: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    count: Optional[int] = None
    material: Optional[str] = None
    unit_mass: Optional[float] = None
    total_mass: Optional[float] = None
    remark: Optional[str] = None

class ComponentsFilter(BaseModel):
    """
    部件查询参数
    """
    project_code: Optional[str] = None
    wtcode: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    material: Optional[str] = None
    remark: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

class ComponentsOut(ComponentsBase):
    """
    部件输出模型
    """
    # id: int
    # created_time: datetime
    # updated_time: datetime    
    model_config = ConfigDict(from_attributes=True)
