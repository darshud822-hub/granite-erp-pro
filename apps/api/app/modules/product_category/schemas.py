from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCategoryBase(BaseModel):
    category_name: str
    category_code: str
    description: str | None = None


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(ProductCategoryBase):
    pass


class ProductCategoryResponse(ProductCategoryBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )