from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
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
    credit_limit: Decimal = 0
    notes: str | None = None

    company_id: UUID
    branch_id: UUID


class CustomerUpdate(BaseModel):
    company_name: str | None = None
    contact_person: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    gst_number: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None
    credit_limit: Decimal | None = None
    notes: str | None = None


class CustomerResponse(BaseModel):
    id: UUID
    customer_code: str
    company_name: str
    contact_person: str
    email: EmailStr
    phone: str
    gst_number: str | None
    credit_limit: Decimal
    outstanding_balance: Decimal

    company_id: UUID
    branch_id: UUID

    class Config:
        from_attributes = True