from sqlalchemy.orm import Session

from app.models.product_category import ProductCategory
from app.modules.product_category.schemas import (
    ProductCategoryCreate,
    ProductCategoryUpdate,
)


def create_category(
    db: Session,
    category: ProductCategoryCreate,
):
    existing = (
        db.query(ProductCategory)
        .filter(
            (ProductCategory.category_name == category.category_name)
            | (ProductCategory.category_code == category.category_code)
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Category name or code already exists"
        )

    new_category = ProductCategory(
        category_name=category.category_name,
        category_code=category.category_code,
        description=category.description,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_categories(db: Session):
    return db.query(ProductCategory).all()


def get_category(
    db: Session,
    category_id,
):
    return (
        db.query(ProductCategory)
        .filter(ProductCategory.id == category_id)
        .first()
    )


def update_category(
    db: Session,
    category_id,
    category: ProductCategoryUpdate,
):
    db_category = get_category(db, category_id)

    if not db_category:
        return None

    db_category.category_name = category.category_name
    db_category.category_code = category.category_code
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(
    db: Session,
    category_id,
):
    category = get_category(db, category_id)

    if not category:
        return False

    db.delete(category)
    db.commit()

    return True