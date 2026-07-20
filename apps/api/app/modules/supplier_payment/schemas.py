from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.supplier_payment import (
    SupplierPaymentMethod,
    SupplierPaymentStatus,
)


class SupplierPaymentBase(BaseModel):
    payment_number: str
    payment_date: date

    purchase_invoice_id: UUID
    supplier_id: UUID

    company_id: UUID
    branch_id: UUID

    payment_method: SupplierPaymentMethod
    amount: Decimal

    reference_number: str | None = None
    remarks: str | None = None


class SupplierPaymentCreate(SupplierPaymentBase):
    pass


class SupplierPaymentUpdate(BaseModel):
    payment_method: SupplierPaymentMethod | None = None
    amount: Decimal | None = None
    reference_number: str | None = None
    remarks: str | None = None
    status: SupplierPaymentStatus | None = None


class SupplierPaymentResponse(SupplierPaymentBase):
    id: UUID
    status: SupplierPaymentStatus

    model_config = ConfigDict(
        from_attributes=True
    )