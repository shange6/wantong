from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base_model import ModelMixin, UserMixin

if TYPE_CHECKING:
    from app.plugin.module_projects.components.model import ComponentsModel

class ProjectsModel(ModelMixin, UserMixin):
    """
    项目表
    """
    __tablename__ = "projects_projects"
    __table_args__ = {"comment": "项目表"}
    
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="项目编码")
    name: Mapped[str] = mapped_column(String(255), comment="项目名称")
    no: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="合同号")
    
    # 关联组件
    components: Mapped[List["ComponentsModel"]] = relationship(
        "ComponentsModel",
        back_populates="projects", 
        cascade="all, delete-orphan"
    )
