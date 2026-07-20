from decimal import Decimal
from uuid import UUID
from pydantic import ConfigDict
from pydantic import BaseModel, EmailStr, ConfigDict


class SupplierBase(BaseModel):
    supplier_code: str
    company_name: str
    contact_person: str
    email: EmailStr
    phone: str
    gst_number: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None
    credit_limit: Decimal = Decimal("0.00")
    outstanding_balance: Decimal = Decimal("0.00")
    notes: str | None = None
    company_id: UUID
    branch_id: UUID


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )