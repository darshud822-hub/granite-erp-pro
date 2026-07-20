from uuid import UUID

from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: str | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None


class DepartmentResponse(BaseModel):
    id: UUID
    name: str
    code: str
    description: str | None

    class Config:
        from_attributes = True