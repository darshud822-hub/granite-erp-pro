from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.supplier.schemas import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
)

from app.modules.supplier.service import (
    create_supplier,
    get_suppliers,
    get_supplier,
    update_supplier,
    delete_supplier,
)

from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/suppliers",
    tags=["Supplier"],
)


@router.post("/", response_model=SupplierResponse)
def create(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_supplier(db, supplier)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[SupplierResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_suppliers(db)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_one(
    supplier_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    supplier = get_supplier(db, supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update(
    supplier_id: str,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    updated = update_supplier(
        db,
        supplier_id,
        supplier,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    return updated


@router.delete("/{supplier_id}")
def delete(
    supplier_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_supplier(
        db,
        supplier_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    return {
        "message": "Supplier deleted successfully"
    }