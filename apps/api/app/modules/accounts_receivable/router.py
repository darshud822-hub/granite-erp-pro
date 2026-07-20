from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.accounts_receivable.schemas import (
    AccountsReceivableCreate,
    AccountsReceivableResponse,
)

from app.modules.accounts_receivable.service import (
    create_accounts_receivable,
    get_accounts_receivables,
    get_accounts_receivable,
    get_customer_receivables,
    delete_accounts_receivable,
)

router = APIRouter(
    prefix="/accounts-receivable",
    tags=["Accounts Receivable"],
)


@router.post("/", response_model=AccountsReceivableResponse)
def create(
    receivable: AccountsReceivableCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    try:
        return create_accounts_receivable(db, receivable)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[AccountsReceivableResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_accounts_receivables(db)


@router.get("/{receivable_id}", response_model=AccountsReceivableResponse)
def get_one(
    receivable_id: UUID,
    db: Session = Depends(get_db),
):
    receivable = get_accounts_receivable(
        db,
        receivable_id,
    )

    if not receivable:
        raise HTTPException(
            status_code=404,
            detail="Accounts Receivable not found",
        )

    return receivable


@router.get("/customer/{customer_id}")
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    return get_customer_receivables(
        db,
        customer_id,
    )


@router.delete("/{receivable_id}")
def delete(
    receivable_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_accounts_receivable(
        db,
        receivable_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Accounts Receivable not found",
        )

    return {
        "message": "Accounts Receivable deleted successfully"
    }