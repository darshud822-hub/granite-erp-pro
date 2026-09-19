from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.journal_entry import JournalEntry, JournalStatus
from app.models.journal_entry_line import JournalEntryLine
def get_trial_balance(db: Session):
    lines = (
        db.query(JournalEntryLine)
        .join(JournalEntry)
        .options(
            joinedload(JournalEntryLine.account),
        )
        .filter(
            JournalEntry.status == JournalStatus.POSTED
        )
        .all()
    )

    accounts = {}

    total_debit = Decimal("0")
    total_credit = Decimal("0")

    for line in lines:
        account = line.account

        if account.id not in accounts:
            accounts[account.id] = {
                "account_id": account.id,
                "account_code": account.account_code,
                "account_name": account.account_name,
                "debit": Decimal("0"),
                "credit": Decimal("0"),
            }

        accounts[account.id]["debit"] += line.debit
        accounts[account.id]["credit"] += line.credit

        total_debit += line.debit
        total_credit += line.credit

    return {
        "accounts": list(accounts.values()),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "is_balanced": total_debit == total_credit,
    }
