from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )