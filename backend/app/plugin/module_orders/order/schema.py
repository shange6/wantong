# app/plugin/module_orders/schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class OrdersFilter(BaseModel):
    """订单查询过滤条件"""
    wtcode: Optional[str] = Field(None, description="万通码")

class OrdersCreate(BaseModel):
    """订单创建模型"""
    wtcode: str = Field(..., description="部件万通码")
    blanking: Optional[datetime] = Field(None, description="下料时间")
    blanking_user: Optional[str] = Field(None, description="下料人员")
    rivetweld: Optional[datetime] = Field(None, description="铆焊时间")
    rivetweld_user: Optional[str] = Field(None, description="铆焊人员")
    machine: Optional[datetime] = Field(None, description="机加时间")
    machine_user: Optional[str] = Field(None, description="机加人员")
    fitting: Optional[datetime] = Field(None, description="装配时间")
    fitting_user: Optional[str] = Field(None, description="装配人员")
    painting: Optional[datetime] = Field(None, description="喷漆时间")
    painting_user: Optional[str] = Field(None, description="喷漆人员")

class OrdersUpdate(BaseModel):
    """订单更新模型"""
    wtcode: Optional[str] = Field(None, description="部件万通码")
    blanking: Optional[datetime] = Field(None, description="下料时间")
    blanking_user: Optional[str] = Field(None, description="下料人员")
    rivetweld: Optional[datetime] = Field(None, description="铆焊时间")
    rivetweld_user: Optional[str] = Field(None, description="铆焊人员")
    machine: Optional[datetime] = Field(None, description="机加时间")
    machine_user: Optional[str] = Field(None, description="机加人员")
    fitting: Optional[datetime] = Field(None, description="装配时间")
    fitting_user: Optional[str] = Field(None, description="装配人员")
    painting: Optional[datetime] = Field(None, description="喷漆时间")
    painting_user: Optional[str] = Field(None, description="喷漆人员")

class OrdersOut(BaseModel):
    """订单返回模型（基础字段）"""
    id: Optional[int] = Field(None, description="订单ID")
    wtcode: str = Field(..., description="部件万通码")
    blanking: Optional[datetime] = Field(None, description="下料时间")
    blanking_user: Optional[str] = Field(None, description="下料人员")
    rivetweld: Optional[datetime] = Field(None, description="铆焊时间")
    rivetweld_user: Optional[str] = Field(None, description="铆焊人员")
    machine: Optional[datetime] = Field(None, description="机加时间")
    machine_user: Optional[str] = Field(None, description="机加人员")
    fitting: Optional[datetime] = Field(None, description="装配时间")
    fitting_user: Optional[str] = Field(None, description="装配人员")
    painting: Optional[datetime] = Field(None, description="喷漆时间")
    painting_user: Optional[str] = Field(None, description="喷漆人员")
    created_time: Optional[datetime] = Field(None, description="创建时间")
    updated_time: Optional[datetime] = Field(None, description="更新时间")
    created_by: Optional[str] = Field(None, description="创建人")
    updated_by: Optional[str] = Field(None, description="更新人")

    class Config:
        from_attributes = True  # 支持从ORM模型验证
