from decimal import Decimal
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, ConfigDict


class StockMovementBase(BaseModel):
    movement_no: str
    movement_type: str

    product_id: UUID
    warehouse_id: UUID
    company_id: UUID
    branch_id: UUID

    quantity: Decimal
    remarks: str | None = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementUpdate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )
class MovementType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    DAMAGE = "DAMAGE"
    TRANSFER = "TRANSFER"
    ADJUSTMENT_IN = "ADJUSTMENT_IN"
    ADJUSTMENT_OUT = "ADJUSTMENT_OUT"
    
movement_type: MovementType