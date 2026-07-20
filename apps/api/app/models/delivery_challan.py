from datetime import date
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class DeliveryStatus(str, Enum):
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class DeliveryChallan(BaseModel):
    __tablename__ = "delivery_challans"

    challan_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    challan_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
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

    status: Mapped[DeliveryStatus] = mapped_column(
        SqlEnum(DeliveryStatus),
        default=DeliveryStatus.PENDING,
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sales_order = relationship("SalesOrder")
    customer = relationship("Customer")
    company = relationship("Company")
    branch = relationship("Branch")

    items = relationship(
        "DeliveryChallanItem",
        back_populates="delivery_challan",
        cascade="all, delete-orphan",
    )