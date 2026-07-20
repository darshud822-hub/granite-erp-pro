from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    product_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
    )

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("product_categories.id"),
        nullable=False,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    purchase_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    minimum_stock: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    reorder_level: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    hsn_code: Mapped[str | None] = mapped_column(
        String(20),
    )

    gst_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=18,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
    )

    weight: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
    )

    dimensions: Mapped[str | None] = mapped_column(
        String(100),
    )

    is_saleable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_purchaseable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    category = relationship(
        "ProductCategory",
        back_populates="products",
    )

    supplier = relationship(
        "Supplier",
        back_populates="products",
    )

    uom = relationship(
        "UOM",
        back_populates="products",
    )

    company = relationship(
        "Company",
    )

    branch = relationship(
        "Branch",
    )
    stocks = relationship(
    "Stock",
    back_populates="product",
)
    purchase_order_items = relationship(
    "PurchaseOrderItem"
)