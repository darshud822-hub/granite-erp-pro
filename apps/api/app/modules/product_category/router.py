from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.product_category.schemas import (
    ProductCategoryCreate,
    ProductCategoryUpdate,
    ProductCategoryResponse,
)

from app.modules.product_category.service import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category,
)

from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/product-categories",
    tags=["Product Categories"],
)


@router.post("/", response_model=ProductCategoryResponse)
def create(
    category: ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_category(db, category)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[ProductCategoryResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_categories(db)


@router.get("/{category_id}", response_model=ProductCategoryResponse)
def get_one(
    category_id: str,
    db: Session = Depends(get_db),
):
    category = get_category(db, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.put("/{category_id}", response_model=ProductCategoryResponse)
def update(
    category_id: str,
    category: ProductCategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    updated = update_category(
        db,
        category_id,
        category,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return updated


@router.delete("/{category_id}")
def delete(
    category_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    deleted = delete_category(
        db,
        category_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return {
        "message": "Category deleted successfully"
    }