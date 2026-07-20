from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StockBase(BaseModel):
    product_id: UUID
    warehouse_id: UUID
    company_id: UUID
    branch_id: UUID

    quantity: Decimal = Decimal("0.00")
    reserved_quantity: Decimal = Decimal("0.00")
    available_quantity: Decimal = Decimal("0.00")
    minimum_stock: Decimal = Decimal("0.00")
    maximum_stock: Decimal = Decimal("0.00")


class StockCreate(StockBase):
    pass


class StockUpdate(StockBase):
    pass


class StockResponse(StockBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )