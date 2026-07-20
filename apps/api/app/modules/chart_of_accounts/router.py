from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.roles import UserRole
from app.db.session import get_db
from app.modules.auth.permissions import require_roles

from app.modules.chart_of_accounts.schemas import (
    ChartOfAccountCreate,
    ChartOfAccountResponse,
    ChartOfAccountUpdate,
)

from app.modules.chart_of_accounts.service import (
    create_chart_of_account,
    get_chart_of_accounts,
    get_chart_of_account,
    get_accounts_by_type,
    update_chart_of_account,
    delete_chart_of_account,
)

router = APIRouter(
    prefix="/chart-of-accounts",
    tags=["Chart of Accounts"],
)


@router.post("/", response_model=ChartOfAccountResponse)
def create(
    account: ChartOfAccountCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    try:
        return create_chart_of_account(db, account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ChartOfAccountResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_chart_of_accounts(db)


@router.get("/{account_id}", response_model=ChartOfAccountResponse)
def get_one(
    account_id: UUID,
    db: Session = Depends(get_db),
):
    account = get_chart_of_account(db, account_id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return account


@router.get("/type/{account_type}")
def get_by_type(
    account_type: str,
    db: Session = Depends(get_db),
):
    return get_accounts_by_type(
        db,
        account_type,
    )


@router.put("/{account_id}", response_model=ChartOfAccountResponse)
def update(
    account_id: UUID,
    account: ChartOfAccountUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    updated = update_chart_of_account(
        db,
        account_id,
        account,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return updated


@router.delete("/{account_id}")
def delete(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    try:
        deleted = delete_chart_of_account(
            db,
            account_id,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Account not found",
            )

        return {
            "message": "Account deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )