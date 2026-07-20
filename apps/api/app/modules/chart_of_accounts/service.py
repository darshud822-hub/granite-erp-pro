from uuid import UUID

from sqlalchemy.orm import Session

from app.models.chart_of_account import ChartOfAccount
from app.modules.chart_of_accounts.schemas import (
    ChartOfAccountCreate,
    ChartOfAccountUpdate,
)
def create_chart_of_account(
    db: Session,
    account: ChartOfAccountCreate,
):
    existing = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.account_code == account.account_code
        )
        .first()
    )

    if existing:
        raise ValueError("Account code already exists.")

    if account.parent_account_id:
        parent = (
            db.query(ChartOfAccount)
            .filter(
                ChartOfAccount.id == account.parent_account_id
            )
            .first()
        )

        if not parent:
            raise ValueError("Parent account not found.")

    coa = ChartOfAccount(**account.model_dump())

    db.add(coa)
    db.commit()
    db.refresh(coa)

    return coa
def get_chart_of_accounts(db: Session):
    return (
        db.query(ChartOfAccount)
        .order_by(ChartOfAccount.account_code)
        .all()
    )


def get_chart_of_account(
    db: Session,
    account_id: UUID,
):
    return (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == account_id
        )
        .first()
    )


def get_accounts_by_type(
    db: Session,
    account_type: str,
):
    return (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.account_type == account_type
        )
        .order_by(ChartOfAccount.account_code)
        .all()
    )
def update_chart_of_account(
    db: Session,
    account_id: UUID,
    update_data: ChartOfAccountUpdate,
):
    account = get_chart_of_account(db, account_id)

    if not account:
        return None

    for key, value in update_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)

    return account
def delete_chart_of_account(
    db: Session,
    account_id: UUID,
):
    account = get_chart_of_account(db, account_id)

    if not account:
        return False

    if account.children:
        raise ValueError(
            "Cannot delete an account that has child accounts."
        )

    db.delete(account)
    db.commit()

    return True