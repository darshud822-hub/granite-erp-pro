from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.sales_invoice import SalesInvoiceStatus


class SalesInvoiceItemBase(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    discount: Decimal = Decimal("0")
    tax_percent: Decimal = Decimal("0")


class SalesInvoiceItemCreate(SalesInvoiceItemBase):
    pass


class SalesInvoiceItemResponse(SalesInvoiceItemBase):
    id: UUID
    line_total: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class SalesInvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: date

    delivery_challan_id: UUID
    customer_id: UUID

    company_id: UUID
    branch_id: UUID

    remarks: str | None = None


class SalesInvoiceCreate(SalesInvoiceBase):
    items: list[SalesInvoiceItemCreate]


class SalesInvoiceUpdate(BaseModel):
    status: SalesInvoiceStatus
    remarks: str | None = None


class SalesInvoiceResponse(SalesInvoiceBase):
    id: UUID

    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal

    status: SalesInvoiceStatus

    items: list[SalesInvoiceItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )