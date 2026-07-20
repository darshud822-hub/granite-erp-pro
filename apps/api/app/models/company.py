from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.customer import Customer
from app.models.base_model import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    logo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    branches: Mapped[list["Branch"]] = relationship(
        "Branch",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    back_populates="company",
    cascade="all, delete-orphan",
    )

    customers: Mapped[list["Customer"]] = relationship(
    "Customer",
    back_populates="company",
    cascade="all, delete-orphan",
)
    suppliers = relationship(
    "Supplier",
    back_populates="company",
    cascade="all, delete-orphan",
)
    warehouses = relationship(
    "Warehouse",
    back_populates="company",
)