# app/plugin/module_orders/schema.py
from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List, Any
from app.core.validator import DateTimeStr, DateStr

class OrdersFilter(BaseModel):
    """订单查询过滤条件"""
    wtcode: Optional[str] = Field(None, description="万通码")
    project_code: Optional[str] = Field(None, description="项目代号")

class OrderBaseModel(BaseModel):
    """订单工序基础模型"""
    is_blanking: bool = Field(False, description="是否下料")
    blanking_time: Optional[DateStr] = Field(None, description="下料时间")
    blanking_user: Optional[str] = Field(None, description="下料班长")
    blanking_laborhour: Optional[int] = Field(None, description="下料工时")
    is_rivetweld: bool = Field(False, description="是否铆焊")
    rivetweld_time: Optional[DateStr] = Field(None, description="铆焊时间")
    rivetweld_user: Optional[str] = Field(None, description="铆焊班长")
    rivetweld_laborhour: Optional[int] = Field(None, description="铆焊工时")
    is_machine: bool = Field(False, description="是否机加")
    machine_time: Optional[DateStr] = Field(None, description="机加时间")
    machine_user: Optional[str] = Field(None, description="机加工班长")
    machine_laborhour: Optional[int] = Field(None, description="机加工时")
    is_fitting: bool = Field(False, description="是否装配")
    fitting_time: Optional[DateStr] = Field(None, description="装配时间")
    fitting_user: Optional[str] = Field(None, description="装配班长")
    fitting_laborhour: Optional[int] = Field(None, description="装配工时")
    is_painting: bool = Field(False, description="是否喷漆")
    painting_time: Optional[DateStr] = Field(None, description="喷漆时间")
    painting_user: Optional[str] = Field(None, description="喷漆班长")
    painting_laborhour: Optional[int] = Field(None, description="喷漆工时")

    # 添加一个通用的预处理校验器
    @field_validator(
        "blanking_time", "blanking_user", 
        "rivetweld_time", "rivetweld_user", 
        "machine_time", "machine_user", 
        "fitting_time", "fitting_user", 
        "painting_time", "painting_user", 
        mode="before"
    )
    @classmethod
    def empty_string_to_none(cls, v):
        # 如果输入是空字符串，强制转换为 None
        if v == "":
            return None
        return v

class OrdersCreate(OrderBaseModel):
    """订单创建模型"""
    wtcode: str = Field(..., description="部件万通码")

class OrdersUpdate(OrderBaseModel):
    """订单更新模型"""
    wtcode: Optional[str] = Field(None, description="部件万通码")

class OrdersOut(OrderBaseModel):
    """订单返回模型（基础字段）"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(None, description="订单ID")
    wtcode: str = Field(..., description="部件万通码")
    code: Optional[str] = Field(None, description="部件代号")
    spec: Optional[str] = Field(None, description="部件规格")
    count: Optional[int] = Field(None, description="部件数量")
    material: Optional[str] = Field(None, description="部件材料")
    unit_mass: Optional[float] = Field(None, description="部件单重")
    total_mass: Optional[float] = Field(None, description="部件总重")
    remark: Optional[str] = Field(None, description="部件备注")
    created_time: Optional[DateTimeStr] = Field(None, description="创建时间")
    updated_time: Optional[DateTimeStr] = Field(None, description="更新时间")
    is_ordered: bool = Field(True, description="是否已排产")

    @model_validator(mode="before")
    @classmethod
    def flatten_component(cls, data: Any) -> Any:
        """从关联的 component 模型中拉取字段并打平，不修改字段名"""
        if hasattr(data, "component") and data.component:
            comp = data.component
            # 提取原始数据中已有的属性
            if not isinstance(data, dict):
                base_data = {c.name: getattr(data, c.name) for c in data.__table__.columns} if hasattr(data, "__table__") else {}
                # 直接将关联组件的字段合并进来，保持原始字段名
                base_data.update({
                    "code": comp.code,
                    "spec": comp.spec,
                    "count": comp.count,
                    "material": comp.material,
                    "unit_mass": comp.unit_mass,
                    "total_mass": comp.total_mass,
                    "remark": comp.remark,
                    "is_ordered": True
                })
                return base_data
        return data

class ComponentsUncreateOut(BaseModel):
    """待创建工单的组件模型（直接使用原始字段名）"""
    model_config = ConfigDict(from_attributes=True)

    wtcode: str = Field(..., description="部件万通码")
    code: Optional[str] = Field(None, description="部件代号")
    spec: Optional[str] = Field(None, description="部件规格")
    count: Optional[int] = Field(None, description="部件数量")
    material: Optional[str] = Field(None, description="部件材料")
    unit_mass: Optional[float] = Field(None, description="部件单重")
    total_mass: Optional[float] = Field(None, description="部件总重")
    remark: Optional[str] = Field(None, description="部件备注")
    is_ordered: bool = Field(False, description="是否已排产")

class OrdersCreateOut(BaseModel):
    """工单创建返回模型"""
    count: int = Field(..., description="新增数量")
    id: int = Field(..., description="新增ID")
    record: OrdersOut = Field(..., description="新增记录")
