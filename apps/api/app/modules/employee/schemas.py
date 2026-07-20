from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    gender: str
    date_of_birth: date
    joining_date: date
    designation: str
    department: str
    salary: Decimal
    address: str | None = None
    company_id: UUID
    branch_id: UUID


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    designation: str | None = None
    department: str | None = None
    salary: Decimal | None = None
    address: str | None = None
    is_active_employee: bool | None = None


class EmployeeResponse(BaseModel):
    id: UUID
    employee_code: str
    full_name: str
    email: EmailStr
    phone: str
    designation: str
    department: str
    salary: Decimal
    company_id: UUID
    branch_id: UUID

    class Config:
        from_attributes = True