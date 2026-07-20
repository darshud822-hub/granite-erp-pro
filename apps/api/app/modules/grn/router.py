from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.grn.schemas import (
    GRNCreate,
    GRNResponse,
)

from app.modules.grn.service import (
    create_grn,
    get_grns,
    get_grn,
    delete_grn,
)

router = APIRouter(
    prefix="/grns",
    tags=["Goods Receipt Notes"],
)


@router.post("/", response_model=GRNResponse)
def create(
    grn: GRNCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_grn(db, grn)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[GRNResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_grns(db)


@router.get("/{grn_id}", response_model=GRNResponse)
def get_one(
    grn_id: UUID,
    db: Session = Depends(get_db),
):
    grn = get_grn(
        db,
        grn_id,
    )

    if not grn:
        raise HTTPException(
            status_code=404,
            detail="GRN not found",
        )

    return grn


@router.delete("/{grn_id}")
def delete(
    grn_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_grn(
        db,
        grn_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="GRN not found",
        )

    return {
        "message": "GRN deleted successfully"
    }