from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Warehouse(BaseModel):
    __tablename__ = "warehouses"

    warehouse_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    warehouse_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    manager_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(300),
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

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    company = relationship(
    "Company",
    back_populates="warehouses",
)
    branch = relationship("Branch")

    stock_items = relationship(
        "Stock",
        back_populates="warehouse",
    )