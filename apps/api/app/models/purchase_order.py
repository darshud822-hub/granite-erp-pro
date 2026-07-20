from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    po_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    po_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("suppliers.id"),
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

    status: Mapped[str] = mapped_column(
        String(30),
        default="DRAFT",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    supplier = relationship("Supplier")
    company = relationship("Company")
    branch = relationship("Branch")

    items = relationship(
        "PurchaseOrderItem",
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )