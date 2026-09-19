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


def get_profit_and_loss(db: Session):
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

    income_accounts = {}
    expense_accounts = {}

    total_income = Decimal("0")
    total_expense = Decimal("0")

    for line in lines:

        account = line.account

        if account.account_type == AccountType.INCOME:

            amount = line.credit - line.debit

            if account.id not in income_accounts:
                income_accounts[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            income_accounts[account.id]["amount"] += amount
            total_income += amount

        elif account.account_type == AccountType.EXPENSE:

            amount = line.debit - line.credit

            if account.id not in expense_accounts:
                expense_accounts[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            expense_accounts[account.id]["amount"] += amount
            total_expense += amount

    return {
        "revenue": list(income_accounts.values()),
        "expenses": list(expense_accounts.values()),
        "total_revenue": total_income,
        "total_expenses": total_expense,
        "net_profit": total_income - total_expense,
    }