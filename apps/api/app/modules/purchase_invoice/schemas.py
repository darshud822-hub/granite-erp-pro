from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PurchaseInvoiceItemBase(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    tax_percent: Decimal = Decimal("0")
    line_total: Decimal


class PurchaseInvoiceItemCreate(PurchaseInvoiceItemBase):
    pass


class PurchaseInvoiceItemResponse(PurchaseInvoiceItemBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class PurchaseInvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: date

    supplier_id: UUID
    grn_id: UUID

    company_id: UUID
    branch_id: UUID

    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal = Decimal("0")
    grand_total: Decimal

    remarks: str | None = None


class PurchaseInvoiceCreate(PurchaseInvoiceBase):
    items: list[PurchaseInvoiceItemCreate]


class PurchaseInvoiceUpdate(PurchaseInvoiceBase):
    pass


class PurchaseInvoiceResponse(PurchaseInvoiceBase):
    id: UUID
    items: list[PurchaseInvoiceItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )