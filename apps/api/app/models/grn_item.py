from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class GRNItem(BaseModel):
    __tablename__ = "grn_items"

    grn_id: Mapped[UUID] = mapped_column(
        ForeignKey("grns.id"),
        nullable=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    received_quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    grn = relationship(
        "GRN",
        back_populates="items",
    )

    product = relationship("Product")