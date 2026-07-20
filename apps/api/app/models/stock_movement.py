from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class StockMovement(BaseModel):
    __tablename__ = "stock_movements"

    movement_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    movement_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

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
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
    String(300),
    nullable=True,
)

    product = relationship("Product")
    warehouse = relationship("Warehouse")
    company = relationship("Company")
    branch = relationship("Branch")