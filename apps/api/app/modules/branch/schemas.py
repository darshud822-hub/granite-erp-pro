from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class BranchCreate(BaseModel):
    company_id: UUID
    name: str
    code: str
    address: Optional[str] = None


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None


class BranchResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    code: str
    address: Optional[str]

    class Config:
        from_attributes = True