from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.warehouse.schemas import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse,
)

from app.modules.warehouse.service import (
    create_warehouse,
    get_warehouses,
    get_warehouse,
    update_warehouse,
    delete_warehouse,
)

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


@router.post("/", response_model=WarehouseResponse)
def create(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_warehouse(db, warehouse)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[WarehouseResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_warehouses(db)


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_one(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
):
    warehouse = get_warehouse(db, warehouse_id)

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found",
        )

    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update(
    warehouse_id: UUID,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    updated = update_warehouse(
        db,
        warehouse_id,
        warehouse,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found",
        )

    return updated


@router.delete("/{warehouse_id}")
def delete(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_warehouse(
        db,
        warehouse_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found",
        )

    return {
        "message": "Warehouse deleted successfully"
    }