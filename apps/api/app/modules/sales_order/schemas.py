from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.sales_order import SalesOrderStatus


class SalesOrderItemBase(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal = Decimal("0")
    tax_percent: Decimal = Decimal("0")


class SalesOrderItemCreate(SalesOrderItemBase):
    pass


class SalesOrderItemResponse(SalesOrderItemBase):
    id: UUID
    line_total: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class SalesOrderBase(BaseModel):
    order_number: str
    order_date: date

    customer_id: UUID
    company_id: UUID
    branch_id: UUID

    remarks: str | None = None


class SalesOrderCreate(SalesOrderBase):
    items: list[SalesOrderItemCreate]


class SalesOrderUpdate(BaseModel):
    remarks: str | None = None
    status: SalesOrderStatus


class SalesOrderResponse(SalesOrderBase):
    id: UUID
    status: SalesOrderStatus
    total_amount: Decimal
    items: list[SalesOrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )