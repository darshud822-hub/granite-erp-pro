from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.delivery_challan import DeliveryStatus


class DeliveryChallanItemBase(BaseModel):
    product_id: UUID
    warehouse_id: UUID
    quantity: Decimal


class DeliveryChallanItemCreate(DeliveryChallanItemBase):
    pass


class DeliveryChallanItemResponse(DeliveryChallanItemBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class DeliveryChallanBase(BaseModel):
    challan_number: str
    challan_date: date

    sales_order_id: UUID
    customer_id: UUID

    company_id: UUID
    branch_id: UUID

    remarks: str | None = None


class DeliveryChallanCreate(DeliveryChallanBase):
    items: list[DeliveryChallanItemCreate]


class DeliveryChallanUpdate(BaseModel):
    status: DeliveryStatus
    remarks: str | None = None


class DeliveryChallanResponse(DeliveryChallanBase):
    id: UUID
    status: DeliveryStatus
    items: list[DeliveryChallanItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )