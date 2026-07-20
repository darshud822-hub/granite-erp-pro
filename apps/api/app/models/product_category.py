from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class ProductCategory(BaseModel):
    __tablename__ = "product_categories"

    category_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    category_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    products = relationship(
        "Product",
        back_populates="category",
    )