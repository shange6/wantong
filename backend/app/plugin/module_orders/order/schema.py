# app/plugin/module_orders/schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.core.validator import DateTimeStr

class OrdersFilter(BaseModel):
    """订单查询过滤条件"""
    wtcode: Optional[str] = Field(None, description="万通码")

class OrderBaseModel(BaseModel):
    """订单工序基础模型"""
    is_blanking: bool = Field(False, description="是否下料")
    blanking_time: Optional[DateTimeStr] = Field(None, description="下料时间")
    blanking_user: Optional[str] = Field(None, description="下料人员")
    is_rivetweld: bool = Field(False, description="是否铆焊")
    rivetweld_time: Optional[DateTimeStr] = Field(None, description="铆焊时间")
    rivetweld_user: Optional[str] = Field(None, description="铆焊人员")
    is_machine: bool = Field(False, description="是否机加")
    machine_time: Optional[DateTimeStr] = Field(None, description="机加时间")
    machine_user: Optional[str] = Field(None, description="机加人员")
    is_fitting: bool = Field(False, description="是否装配")
    fitting_time: Optional[DateTimeStr] = Field(None, description="装配时间")
    fitting_user: Optional[str] = Field(None, description="装配人员")
    is_painting: bool = Field(False, description="是否喷漆")
    painting_time: Optional[DateTimeStr] = Field(None, description="喷漆时间")
    painting_user: Optional[str] = Field(None, description="喷漆人员")

class OrdersCreate(OrderBaseModel):
    """订单创建模型"""
    wtcode: str = Field(..., description="部件万通码")

class OrdersUpdate(OrderBaseModel):
    """订单更新模型"""
    wtcode: Optional[str] = Field(None, description="部件万通码")

class OrdersOut(OrderBaseModel):
    """订单返回模型（基础字段）"""
    id: Optional[int] = Field(None, description="订单ID")
    wtcode: str = Field(..., description="部件万通码")
    created_time: Optional[DateTimeStr] = Field(None, description="创建时间")
    updated_time: Optional[DateTimeStr] = Field(None, description="更新时间")

    class Config:
        from_attributes = True  # 支持从ORM模型验证

class OrdersCreateOut(BaseModel):
    """工单创建返回模型"""
    count: int = Field(..., description="新增数量")
    id: int = Field(..., description="新增ID")
    record: OrdersOut = Field(..., description="新增记录")
