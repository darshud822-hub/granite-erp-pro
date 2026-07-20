from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.branch.schemas import (
    BranchCreate,
    BranchUpdate,
    BranchResponse,
)
from app.modules.branch.service import (
    create_branch,
    get_branches,
    get_branch,
    update_branch,
    delete_branch,
)

from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/branches",
    tags=["Branches"],
)


@router.post(
    "/",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    branch: BranchCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    try:
        return create_branch(db, branch)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[BranchResponse],
)
def get_all(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_branches(db)


@router.get(
    "/{branch_id}",
    response_model=BranchResponse,
)
def get_one(
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    branch = get_branch(db, branch_id)

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found",
        )

    return branch


@router.put(
    "/{branch_id}",
    response_model=BranchResponse,
)
def update(
    branch_id: UUID,
    data: BranchUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    branch = update_branch(db, branch_id, data)

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found",
        )

    return branch


@router.delete("/{branch_id}")
def delete(
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    branch = delete_branch(db, branch_id)

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found",
        )

    return {
        "message": "Branch deleted successfully"
    }