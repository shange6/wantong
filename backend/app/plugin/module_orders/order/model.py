from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base_model import ModelMixin, UserMixin
from datetime import datetime

if TYPE_CHECKING:
    from app.plugin.module_projects.components.model import ComponentsModel
    # from app.plugin.module_projects.parts.model import PartsModel

class OrdersModel(ModelMixin, UserMixin):
    """
    订单表
    """
    __tablename__ = "orders_components"
    __table_args__ = {"comment": "订单表"}  
    
    wtcode: Mapped[str] = mapped_column(String(64), ForeignKey("projects_components.wtcode"), unique=True, index=True, nullable=False, comment="部件万通码")
    is_blanking: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否下料")
    blanking_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="下料时间")
    blanking_user: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="下料人员")
    is_rivetweld: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否铆焊")
    rivetweld_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="铆焊时间")
    rivetweld_user: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="铆焊人员")
    is_machine: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否机加")
    machine_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="机加时间")
    machine_user: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="机加人员")
    is_fitting: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否装配")
    fitting_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="装配时间")
    fitting_user: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="装配人员")
    is_painting: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否喷漆")
    painting_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="喷漆时间")
    painting_user: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="喷漆人员")

    # # 关联组件
    component: Mapped["ComponentsModel"] = relationship("ComponentsModel", back_populates="order")
