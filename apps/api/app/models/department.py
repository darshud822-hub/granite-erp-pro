from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

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
        String(255),
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="department",
    )