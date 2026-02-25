from typing import TYPE_CHECKING, Annotated
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base_model import ModelMixin, UserMixin
from datetime import datetime

if TYPE_CHECKING:
    from app.plugin.module_projects.components.model import ComponentsModel

# 定义常用列类型以简化模型定义
Str64 = Annotated[str | None, mapped_column(String(64), nullable=True)]
BoolFalse = Annotated[bool, mapped_column(Boolean, default=False, nullable=False)]
DtNull = Annotated[datetime | None, mapped_column(DateTime, nullable=True)]

class OrdersModel(ModelMixin, UserMixin):
    """
    工单表
    """
    __tablename__ = "orders_components"
    __table_args__ = {"comment": "工单表"}  
    
    wtcode: Mapped[str] = mapped_column(String(64), ForeignKey("projects_components.wtcode"), unique=True, index=True, nullable=False, comment="部件万通码")
    
    # 下料工序
    is_blanking: Mapped[BoolFalse] = mapped_column(comment="是否下料")
    blanking_time: Mapped[DtNull] = mapped_column(comment="下料时间")
    blanking_user: Mapped[Str64] = mapped_column(comment="下料人员")
    blanking_laborhour: Mapped[int | None] = mapped_column(comment="下料工时")
    
    # 铆焊工序
    is_rivetweld: Mapped[BoolFalse] = mapped_column(comment="是否铆焊")
    rivetweld_time: Mapped[DtNull] = mapped_column(comment="铆焊时间")
    rivetweld_user: Mapped[Str64] = mapped_column(comment="铆焊人员")
    rivetweld_laborhour: Mapped[int | None] = mapped_column(comment="铆焊工时")
    
    # 机加工序
    is_machine: Mapped[BoolFalse] = mapped_column(comment="是否机加")
    machine_time: Mapped[DtNull] = mapped_column(comment="机加时间")
    machine_user: Mapped[Str64] = mapped_column(comment="机加人员")
    machine_laborhour: Mapped[int | None] = mapped_column(comment="机加工时")
    
    # 装配工序
    is_fitting: Mapped[BoolFalse] = mapped_column(comment="是否装配")
    fitting_time: Mapped[DtNull] = mapped_column(comment="装配时间")
    fitting_user: Mapped[Str64] = mapped_column(comment="装配人员")
    fitting_laborhour: Mapped[int | None] = mapped_column(comment="装配工时")
    
    # 喷漆工序
    is_painting: Mapped[BoolFalse] = mapped_column(comment="是否喷漆")
    painting_time: Mapped[DtNull] = mapped_column(comment="喷漆时间")
    painting_user: Mapped[Str64] = mapped_column(comment="喷漆人员")
    painting_laborhour: Mapped[int | None] = mapped_column(comment="喷漆工时")

    # 关联组件
    component: Mapped["ComponentsModel"] = relationship("ComponentsModel", back_populates="order")
