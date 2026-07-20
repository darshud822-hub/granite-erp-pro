from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GRNItemBase(BaseModel):
    product_id: UUID
    received_quantity: Decimal


class GRNItemCreate(GRNItemBase):
    pass


class GRNItemResponse(GRNItemBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class GRNBase(BaseModel):
    grn_number: str
    grn_date: date

    purchase_order_id: UUID
    warehouse_id: UUID

    company_id: UUID
    branch_id: UUID

    remarks: str | None = None


class GRNCreate(GRNBase):
    items: list[GRNItemCreate]


class GRNUpdate(GRNBase):
    pass


class GRNResponse(GRNBase):
    id: UUID
    items: list[GRNItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )