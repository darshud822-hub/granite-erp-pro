from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    name: str
    code: str
    gst_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    logo: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    gst_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    logo: Optional[str] = None


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    code: str
    gst_number: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pincode: Optional[str]
    logo: Optional[str]

    class Config:
        from_attributes = True