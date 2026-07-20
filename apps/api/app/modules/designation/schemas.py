from pydantic import BaseModel


class DesignationCreate(BaseModel):
    name: str
    code: str
    description: str | None = None


class DesignationUpdate(BaseModel):
    name: str
    code: str
    description: str | None = None


class DesignationResponse(BaseModel):
    id: str
    name: str
    code: str
    description: str | None = None

    class Config:
        from_attributes = True