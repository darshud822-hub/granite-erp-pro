from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class SupplierPaymentMethod(str, Enum):
    CASH = "CASH"
    BANK = "BANK"
    UPI = "UPI"
    CHEQUE = "CHEQUE"


class SupplierPaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SupplierPayment(BaseModel):
    __tablename__ = "supplier_payments"

    payment_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=False,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("suppliers.id"),
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

    payment_method: Mapped[SupplierPaymentMethod] = mapped_column(
        SqlEnum(SupplierPaymentMethod),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status: Mapped[SupplierPaymentStatus] = mapped_column(
        SqlEnum(SupplierPaymentStatus),
        default=SupplierPaymentStatus.COMPLETED,
        nullable=False,
    )

    purchase_invoice = relationship("PurchaseInvoice")
    supplier = relationship("Supplier")
    company = relationship("Company")
    branch = relationship("Branch")