from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.designation import Designation
from app.modules.designation.schemas import (
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse,
)
from app.modules.designation.service import (
    create_designation,
    get_designations,
    get_designation,
    update_designation,
    delete_designation,
)

from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/designations",
    tags=["Designation"],
)


@router.post(
    "/",
    response_model=DesignationResponse,
)
def create(
    designation: DesignationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_designation(db, designation)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[DesignationResponse],
)
def get_all(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return get_designations(db)


@router.get(
    "/{designation_id}",
    response_model=DesignationResponse,
)
def get_one(
    designation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    designation = get_designation(db, designation_id)

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return designation


@router.put(
    "/{designation_id}",
    response_model=DesignationResponse,
)
def update(
    designation_id: str,
    designation: DesignationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    updated = update_designation(
        db,
        designation_id,
        designation,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return updated


@router.delete("/{designation_id}")
def delete(
    designation_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    deleted = delete_designation(
        db,
        designation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return {
        "message": "Designation deleted successfully"
    }