from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.product.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.modules.product.service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_product(db, product)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[ProductResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_one(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update(
    product_id: UUID,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    updated = update_product(
        db,
        product_id,
        product,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return updated


@router.delete("/{product_id}")
def delete(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_product(
        db,
        product_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "message": "Product deleted successfully"
    }