from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Supplier(BaseModel):
    __tablename__ = "suppliers"

    supplier_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    contact_person: Mapped[str] = mapped_column(
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
        unique=True,
        nullable=False,
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
    )

    credit_limit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    outstanding_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    notes: Mapped[str | None] = mapped_column(
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

    company = relationship(
        "Company",
        back_populates="suppliers",
    )

    branch = relationship(
        "Branch",
        back_populates="suppliers",
    )
    products = relationship(
    "Product",
    back_populates="supplier",
    )