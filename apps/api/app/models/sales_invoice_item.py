from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class SalesInvoiceItem(BaseModel):
    __tablename__ = "sales_invoice_items"

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
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

    discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    tax_percent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=0,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    sales_invoice = relationship(
        "SalesInvoice",
        back_populates="items",
    )

    product = relationship("Product")