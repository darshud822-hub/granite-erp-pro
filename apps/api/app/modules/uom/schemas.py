from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UOMBase(BaseModel):
    name: str
    code: str
    description: str | None = None


class UOMCreate(UOMBase):
    pass


class UOMUpdate(UOMBase):
    pass


class UOMResponse(UOMBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )
    