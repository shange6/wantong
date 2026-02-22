from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
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
    
    wtcode: Mapped[str] = mapped_column(String(64), ForeignKey("projects_components.wtcode"), unique=True, index=True, comment="部件万通码")
    blanking: Mapped[datetime] = mapped_column(DateTime, comment="下料时间")
    rivetweld: Mapped[datetime] = mapped_column(DateTime, comment="铆焊时间")
    machine: Mapped[datetime] = mapped_column(DateTime, comment="机加时间")
    fitting: Mapped[datetime] = mapped_column(DateTime, comment="装配时间")
    painting: Mapped[datetime] = mapped_column(DateTime, comment="喷漆时间")

    # # 关联组件
    # component: Mapped["ComponentsModel"] = relationship("ComponentsModel", back_populates="orders_components")
