from datetime import date
from decimal import Decimal
from enum import Enum                  # Python Enum ✅
from sqlalchemy import Enum as SqlEnum # SQLAlchemy Enum ✅
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

class PurchaseInvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
class PurchaseInvoice(BaseModel):
    __tablename__ = "purchase_invoices"

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

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    grn_id: Mapped[UUID] = mapped_column(
        ForeignKey("grns.id"),
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
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )
    paid_amount: Mapped[Decimal] = mapped_column(
    Numeric(12, 2),
    default=0,
)

    balance_amount: Mapped[Decimal] = mapped_column(
    Numeric(12, 2),
    default=0,
)

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    supplier = relationship("Supplier")
    grn = relationship("GRN")
    company = relationship("Company")
    branch = relationship("Branch")

    items = relationship(
        "PurchaseInvoiceItem",
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )