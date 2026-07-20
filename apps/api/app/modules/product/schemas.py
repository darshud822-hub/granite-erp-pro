from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    product_code: str
    product_name: str
    description: str | None = None

    category_id: UUID
    supplier_id: UUID
    uom_id: UUID
    company_id: UUID
    branch_id: UUID

    purchase_price: Decimal = Decimal("0.00")
    selling_price: Decimal = Decimal("0.00")

    minimum_stock: Decimal = Decimal("0.00")
    reorder_level: Decimal = Decimal("0.00")

    hsn_code: str | None = None
    gst_percentage: Decimal = Decimal("18.00")

    barcode: str | None = None
    weight: Decimal | None = None
    dimensions: str | None = None

    is_saleable: bool = True
    is_purchaseable: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )