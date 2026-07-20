from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PaymentMethod(str, Enum):
    CASH = "CASH"
    BANK = "BANK"
    UPI = "UPI"
    CHEQUE = "CHEQUE"


class CustomerPaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class CustomerPayment(BaseModel):
    __tablename__ = "customer_payments"

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

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
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

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SqlEnum(PaymentMethod),
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

    status: Mapped[CustomerPaymentStatus] = mapped_column(
        SqlEnum(CustomerPaymentStatus),
        default=CustomerPaymentStatus.COMPLETED,
        nullable=False,
    )

    sales_invoice = relationship("SalesInvoice")
    customer = relationship("Customer")
    company = relationship("Company")
    branch = relationship("Branch")