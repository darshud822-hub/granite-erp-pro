from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.customer_payment import (
    PaymentMethod,
    CustomerPaymentStatus,
)


class CustomerPaymentBase(BaseModel):
    payment_number: str
    payment_date: date

    sales_invoice_id: UUID
    customer_id: UUID

    company_id: UUID
    branch_id: UUID

    payment_method: PaymentMethod
    amount: Decimal

    reference_number: str | None = None
    remarks: str | None = None


class CustomerPaymentCreate(CustomerPaymentBase):
    pass


class CustomerPaymentUpdate(BaseModel):
    payment_method: PaymentMethod | None = None
    amount: Decimal | None = None
    reference_number: str | None = None
    remarks: str | None = None
    status: CustomerPaymentStatus | None = None


class CustomerPaymentResponse(CustomerPaymentBase):
    id: UUID
    status: CustomerPaymentStatus

    model_config = ConfigDict(
        from_attributes=True
    )