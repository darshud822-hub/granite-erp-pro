from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class DeliveryChallanItem(BaseModel):
    __tablename__ = "delivery_challan_items"

    delivery_challan_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_challans.id"),
        nullable=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    delivery_challan = relationship(
        "DeliveryChallan",
        back_populates="items",
    )

    product = relationship("Product")
    warehouse = relationship("Warehouse")