from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base_model import ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.plugin.module_projects.components.model import ComponentsModel

class PartsModel(ModelMixin, UserMixin):
    """
    零件表
    """
    __tablename__ = "projects_parts"
    __table_args__ = {"comment": "零件表"}
    
    component_wtcode: Mapped[str] = mapped_column(
        String(64), 
        ForeignKey("projects_components.wtcode"), 
        comment="部件万通码"
    )
    
    wtcode: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="万通码")
    code: Mapped[str | None] = mapped_column(String(64), comment="编码")
    spec: Mapped[str | None] = mapped_column(String(255), comment="规格")
    count: Mapped[int] = mapped_column(Integer, comment="数量")
    material: Mapped[str | None] = mapped_column(String(255), comment="材质")
    unit_mass: Mapped[float | None] = mapped_column(Float, comment="单重")
    total_mass: Mapped[float | None] = mapped_column(Float, comment="总重")
    remark: Mapped[str | None] = mapped_column(String(500), comment="备注")
    
    # 关联组件
    component: Mapped["ComponentsModel"] = relationship("ComponentsModel", back_populates="parts")
