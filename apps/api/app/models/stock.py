from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Stock(BaseModel):
    __tablename__ = "stocks"

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    reserved_quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    available_quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    minimum_stock: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    maximum_stock: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    product = relationship(
        "Product",
        back_populates="stocks",
    )

    warehouse = relationship(
        "Warehouse",
        back_populates="stock_items",
    )

    company = relationship("Company")
    branch = relationship("Branch")