from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WarehouseBase(BaseModel):
    warehouse_code: str
    warehouse_name: str

    company_id: UUID
    branch_id: UUID

    manager_name: str | None = None
    phone: str | None = None
    email: str | None = None

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None

    remarks: str | None = None


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )