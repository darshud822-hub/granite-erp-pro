from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class GRN(BaseModel):
    __tablename__ = "grns"

    grn_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    grn_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
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

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    purchase_order = relationship("PurchaseOrder")
    warehouse = relationship("Warehouse")
    company = relationship("Company")
    branch = relationship("Branch")

    items = relationship(
        "GRNItem",
        back_populates="grn",
        cascade="all, delete-orphan",
    )
    purchase_order = relationship(
    "PurchaseOrder",
    back_populates="grns",
)