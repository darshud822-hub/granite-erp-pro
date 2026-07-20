from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.uom.schemas import (
    UOMCreate,
    UOMUpdate,
    UOMResponse,
)

from app.modules.uom.service import (
    create_uom,
    get_uoms,
    get_uom,
    update_uom,
    delete_uom,
)

router = APIRouter(
    prefix="/uoms",
    tags=["Unit of Measure"],
)


@router.post("/", response_model=UOMResponse)
def create(
    uom: UOMCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_uom(db, uom)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[UOMResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_uoms(db)


@router.get("/{uom_id}", response_model=UOMResponse)
def get_one(
    uom_id: str,
    db: Session = Depends(get_db),
):
    uom = get_uom(db, uom_id)

    if not uom:
        raise HTTPException(
            status_code=404,
            detail="UOM not found",
        )

    return uom


@router.put("/{uom_id}", response_model=UOMResponse)
def update(
    uom_id: str,
    uom: UOMUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    updated = update_uom(
        db,
        uom_id,
        uom,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="UOM not found",
        )

    return updated


@router.delete("/{uom_id}")
def delete(
    uom_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_uom(
        db,
        uom_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="UOM not found",
        )

    return {
        "message": "UOM deleted successfully"
    }