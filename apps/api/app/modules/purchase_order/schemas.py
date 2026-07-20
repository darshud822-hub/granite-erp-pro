from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PurchaseOrderItemBase(BaseModel):
    product_id: UUID
    quantity: Decimal
    unit_price: Decimal
    tax_percent: Decimal = Decimal("0.00")


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass


class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class PurchaseOrderBase(BaseModel):
    po_number: str
    po_date: date

    supplier_id: UUID
    company_id: UUID
    branch_id: UUID

    status: str = "DRAFT"
    remarks: str | None = None


class PurchaseOrderCreate(PurchaseOrderBase):
    items: list[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(PurchaseOrderBase):
    pass


class PurchaseOrderResponse(PurchaseOrderBase):
    id: UUID
    items: list[PurchaseOrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )