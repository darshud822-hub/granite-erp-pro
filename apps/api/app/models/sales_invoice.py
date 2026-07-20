from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class SalesInvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class SalesInvoice(BaseModel):
    __tablename__ = "sales_invoices"

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    delivery_challan_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_challans.id"),
        nullable=False,
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    status: Mapped[SalesInvoiceStatus] = mapped_column(
        SqlEnum(SalesInvoiceStatus),
        default=SalesInvoiceStatus.DRAFT,
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    paid_amount: Mapped[Decimal] = mapped_column(
    Numeric(12, 2),
    default=0,
)

    balance_amount: Mapped[Decimal] = mapped_column(
    Numeric(12, 2),
    default=0,
)
    delivery_challan = relationship("DeliveryChallan")
    customer = relationship("Customer")
    company = relationship("Company")
    branch = relationship("Branch")

    items = relationship(
        "SalesInvoiceItem",
        back_populates="sales_invoice",
        cascade="all, delete-orphan",
    )