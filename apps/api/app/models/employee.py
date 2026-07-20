from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import (
    String,
    Date,
    Numeric,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Employee(BaseModel):
    __tablename__ = "employees"

    employee_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    department_id: Mapped[UUID] = mapped_column(
    ForeignKey("departments.id"),
    nullable=False,
    )

    department = relationship(
    "Department",
    back_populates="employees",
    )
    designation_id: Mapped[UUID] = mapped_column(
    ForeignKey("designations.id"),
    nullable=False,
   )
    designation = relationship(
    "Designation",
    back_populates="employees",
    )
    

    salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    is_active_employee: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    company = relationship(
        "Company",
        back_populates="employees",
    )

    branch = relationship(
        "Branch",
        back_populates="employees",
    )