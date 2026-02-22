from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base_model import ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.plugin.module_projects.projects.model import ProjectsModel
    from app.plugin.module_projects.parts.model import PartsModel

class ComponentsModel(ModelMixin, UserMixin):
    """
    部件表
    """
    __tablename__ = "projects_components"
    __table_args__ = {"comment": "部件表"}
    
    project_code: Mapped[str] = mapped_column(
        String(64), 
        ForeignKey("projects_projects.code"), 
        comment="项目编码"
    )
    wtcode: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="万通码")
    code: Mapped[str] = mapped_column(String(64), comment="代号")
    spec: Mapped[str] = mapped_column(String(255), comment="规格")
    count: Mapped[int] = mapped_column(Integer, comment="数量")
    material:Mapped[str] = mapped_column(String(255), comment="材料")
    unit_mass: Mapped[float | None] = mapped_column(Float, comment="单重")
    total_mass: Mapped[float | None] = mapped_column(Float, comment="总重")
    remark: Mapped[str | None] = mapped_column(String(500), comment="备注")
    
    # 关联项目
    projects: Mapped["ProjectsModel"] = relationship("ProjectsModel", back_populates="components")
    
    # 关联明细
    parts: Mapped[List["PartsModel"]] = relationship(
        "PartsModel",
        back_populates="component",
        cascade="all, delete-orphan"
    )
    # orders_components: Mapped[list["OrdersModel"]] = relationship(
    #     "OrdersModel",  # 关联的模型类名
    #     back_populates="component",  # 反向关联 OrderModel 中的 component 属性
    #     lazy="selectin"  # 可选：优化查询，避免N+1问题
    # )
