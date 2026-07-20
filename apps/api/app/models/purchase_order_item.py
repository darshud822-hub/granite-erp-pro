from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PurchaseOrderItem(BaseModel):
    __tablename__ = "purchase_order_items"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    tax_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    purchase_order = relationship(
        "PurchaseOrder",
        back_populates="items",
    )

    product = relationship("Product")