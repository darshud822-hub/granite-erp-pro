from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.chart_of_account import (
    AccountType,
)
from app.models.journal_entry import (
    JournalEntry,
    JournalStatus,
)
from app.models.journal_entry_line import (
    JournalEntryLine,
)


def get_balance_sheet(db: Session):
    lines = (
        db.query(JournalEntryLine)
        .join(JournalEntry)
        .options(
            joinedload(JournalEntryLine.account)
        )
        .filter(
            JournalEntry.status == JournalStatus.POSTED
        )
        .all()
    )

    assets = {}
    liabilities = {}
    equity = {}

    total_assets = Decimal("0")
    total_liabilities = Decimal("0")
    total_equity = Decimal("0")

    for line in lines:

        account = line.account

        if account.account_type == AccountType.ASSET:

            amount = line.debit - line.credit

            if account.id not in assets:
                assets[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            assets[account.id]["amount"] += amount
            total_assets += amount

        elif account.account_type == AccountType.LIABILITY:

            amount = line.credit - line.debit

            if account.id not in liabilities:
                liabilities[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            liabilities[account.id]["amount"] += amount
            total_liabilities += amount

        elif account.account_type == AccountType.EQUITY:

            amount = line.credit - line.debit

            if account.id not in equity:
                equity[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            equity[account.id]["amount"] += amount
            total_equity += amount

    total_liabilities_and_equity = (
        total_liabilities + total_equity
    )

    return {
        "assets": list(assets.values()),
        "liabilities": list(liabilities.values()),
        "equity": list(equity.values()),
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "total_liabilities_and_equity": total_liabilities_and_equity,
        "is_balanced": (
            total_assets == total_liabilities_and_equity
        ),
    }