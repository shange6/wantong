from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_model import ModelMixin, UserMixin

class OrderProjectModel(ModelMixin, UserMixin):
    """
    订单项目表
    """
    __tablename__ = "orders_project"
    __table_args__ = {"comment": "订单项目表"}
    
    project_name: Mapped[str | None] = mapped_column(String(255), comment="项目名称")
    project_code: Mapped[str | None] = mapped_column(String(64), comment="项目编码")
    contract_no: Mapped[str | None] = mapped_column(String(64), comment="合同号")
    
    # 关联组件
    components: Mapped[List["OrderComponentModel"]] = relationship(
        back_populates="project", 
        cascade="all, delete-orphan"
    )


class OrderComponentModel(ModelMixin, UserMixin):
    """
    订单组件表
    """
    __tablename__ = "orders_component"
    __table_args__ = {"comment": "订单组件表"}
    
    project_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("orders_project.id"), 
        comment="项目ID"
    )
    
    parent_code: Mapped[str | None] = mapped_column(String(64), comment="父级编码")
    component_name: Mapped[str | None] = mapped_column(String(255), comment="组件名称")
    component_code: Mapped[str | None] = mapped_column(String(64), comment="组件编码")
    component_count: Mapped[int | None] = mapped_column(Integer, comment="组件数量")
    
    # 关联项目
    project: Mapped["OrderProjectModel"] = relationship(back_populates="components")
    
    # 关联明细
    details: Mapped[List["OrderDetailModel"]] = relationship(
        back_populates="component",
        cascade="all, delete-orphan"
    )


class OrderDetailModel(ModelMixin, UserMixin):
    """
    订单明细表
    """
    __tablename__ = "orders_detail"
    __table_args__ = {"comment": "订单明细表"}
    
    component_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("orders_component.id"), 
        comment="组件ID"
    )
    
    wtcode: Mapped[str | None] = mapped_column(String(64), comment="WT编码")
    code: Mapped[str | None] = mapped_column(String(64), comment="编码")
    spec: Mapped[str | None] = mapped_column(String(255), comment="规格")
    count: Mapped[str | None] = mapped_column(String(64), comment="数量")  # schema uses Union[str, int], storing as string for flexibility or convert
    material: Mapped[str | None] = mapped_column(String(255), comment="材质")
    unit_mass: Mapped[float | None] = mapped_column(Float, comment="单重")
    total_mass: Mapped[float | None] = mapped_column(Float, comment="总重")
    remark: Mapped[str | None] = mapped_column(String(500), comment="备注")
    
    # 关联组件
    component: Mapped["OrderComponentModel"] = relationship(back_populates="details")
