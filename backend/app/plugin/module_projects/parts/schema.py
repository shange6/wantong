from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class PartsSchema(BaseModel):
    """
    Parts base schema
    """
    wtcode: str = Field(..., description="万通码")
    code: Optional[str] = Field(None, description="代号")
    spec: Optional[str] = Field(None, description="规格")
    count: Optional[int] = Field(None, description="数量")
    material: Optional[str] = Field(None, description="材质")
    unit_mass: Optional[float] = Field(None, description="单重")
    total_mass: Optional[float] = Field(None, description="总重")
    remark: Optional[str] = Field(None, description="备注")
    component_wtcode: Optional[str] = Field(None, description="部件万通码")

class PartsCreate(PartsSchema):
    """
    Parts create schema
    """
    pass

class PartsUpdate(BaseModel):
    """
    Parts update schema
    """
    code: Optional[str] = Field(None, description="编码")
    spec: Optional[str] = Field(None, description="规格")
    count: Optional[int] = Field(None, description="数量")
    material: Optional[str] = Field(None, description="材质")
    unit_mass: Optional[float] = Field(None, description="单重")
    total_mass: Optional[float] = Field(None, description="总重")
    remark: Optional[str] = Field(None, description="备注")

class PartsFilter(BaseModel):
    """
    Parts filter schema
    """
    wtcode: Optional[str] = Field(None, description="WT编码")
    component_wtcode: Optional[str] = Field(None, description="组件万通编码")
    code: Optional[str] = Field(None, description="编码")
    
    model_config = ConfigDict(extra="ignore")

class PartsOut(PartsSchema):
    """
    Parts output schema
    """    
    # id: int
    # created_time: datetime
    # updated_time: datetime
    
    model_config = ConfigDict(from_attributes=True)
