from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class Designation(BaseModel):
    __tablename__ = "designations"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255)
    )
    employees = relationship(
    "Employee",
    back_populates="designation",
)
    
    