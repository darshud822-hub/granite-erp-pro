from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.stock_movement.schemas import (
    StockMovementCreate,
    StockMovementResponse,
)

from app.modules.stock_movement.service import (
    create_stock_movement,
    get_movements,
    get_movement,
    delete_movement,
)

router = APIRouter(
    prefix="/stock-movements",
    tags=["Stock Movements"],
)


@router.post("/", response_model=StockMovementResponse)
def create(
    movement: StockMovementCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_stock_movement(
            db,
            movement,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[StockMovementResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_movements(db)


@router.get("/{movement_id}", response_model=StockMovementResponse)
def get_one(
    movement_id: UUID,
    db: Session = Depends(get_db),
):
    movement = get_movement(
        db,
        movement_id,
    )

    if not movement:
        raise HTTPException(
            status_code=404,
            detail="Movement not found",
        )

    return movement


@router.delete("/{movement_id}")
def delete(
    movement_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_movement(
        db,
        movement_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Movement not found",
        )

    return {
        "message": "Movement deleted successfully"
    }