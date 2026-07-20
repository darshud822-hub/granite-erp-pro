from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.accounts_payable.schemas import (
    AccountsPayableCreate,
    AccountsPayableResponse,
)

from app.modules.accounts_payable.service import (
    create_accounts_payable,
    get_accounts_payables,
    get_accounts_payable,
    get_supplier_payables,
    delete_accounts_payable,
)

router = APIRouter(
    prefix="/accounts-payable",
    tags=["Accounts Payable"],
)


@router.post("/", response_model=AccountsPayableResponse)
def create(
    payable: AccountsPayableCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.PURCHASE,
        )
    ),
):
    try:
        return create_accounts_payable(db, payable)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[AccountsPayableResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_accounts_payables(db)


@router.get("/{payable_id}", response_model=AccountsPayableResponse)
def get_one(
    payable_id: UUID,
    db: Session = Depends(get_db),
):
    payable = get_accounts_payable(
        db,
        payable_id,
    )

    if not payable:
        raise HTTPException(
            status_code=404,
            detail="Accounts Payable not found",
        )

    return payable


@router.get("/supplier/{supplier_id}")
def get_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
):
    return get_supplier_payables(
        db,
        supplier_id,
    )


@router.delete("/{payable_id}")
def delete(
    payable_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_accounts_payable(
        db,
        payable_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Accounts Payable not found",
        )

    return {
        "message": "Accounts Payable deleted successfully"
    }