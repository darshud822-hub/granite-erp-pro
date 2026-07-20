from sqlalchemy.orm import Session

from app.models.product import Product
from app.modules.product.schemas import (
    ProductCreate,
    ProductUpdate,
)


def create_product(
    db: Session,
    product: ProductCreate,
):
    existing = (
        db.query(Product)
        .filter(
            Product.product_code == product.product_code
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Product code already exists"
        )

    new_product = Product(
        product_code=product.product_code,
        product_name=product.product_name,
        description=product.description,
        category_id=product.category_id,
        supplier_id=product.supplier_id,
        uom_id=product.uom_id,
        company_id=product.company_id,
        branch_id=product.branch_id,
        purchase_price=product.purchase_price,
        selling_price=product.selling_price,
        minimum_stock=product.minimum_stock,
        reorder_level=product.reorder_level,
        hsn_code=product.hsn_code,
        gst_percentage=product.gst_percentage,
        barcode=product.barcode,
        weight=product.weight,
        dimensions=product.dimensions,
        is_saleable=product.is_saleable,
        is_purchaseable=product.is_purchaseable,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_products(db: Session):
    return db.query(Product).all()


def get_product(
    db: Session,
    product_id,
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


def update_product(
    db: Session,
    product_id,
    product: ProductUpdate,
):
    db_product = get_product(
        db,
        product_id,
    )

    if not db_product:
        return None

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(
    db: Session,
    product_id,
):
    db_product = get_product(
        db,
        product_id,
    )

    if not db_product:
        return False

    db.delete(db_product)
    db.commit()

    return True