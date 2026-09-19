from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.journal_entry import JournalEntry, JournalStatus
from app.models.journal_entry_line import JournalEntryLine
def get_general_ledger(
    db: Session,
    account_id: UUID,
):
    lines = (
        db.query(JournalEntryLine)
        .join(JournalEntry)
        .options(
            joinedload(JournalEntryLine.account),
            joinedload(JournalEntryLine.journal_entry),
        )
        .filter(
            JournalEntryLine.account_id == account_id,
            JournalEntry.status == JournalStatus.POSTED,
        )
        .order_by(
            JournalEntry.created_at
        )
        .all()
    )

    running_balance = Decimal("0")

    ledger = []

    total_debit = Decimal("0")
    total_credit = Decimal("0")

    for line in lines:

        total_debit += line.debit
        total_credit += line.credit

        running_balance += line.debit
        running_balance -= line.credit

        ledger.append(
            {
                "journal_number": line.journal_entry.journal_number,
                "transaction_date": line.journal_entry.created_at,
                "account_id": line.account.id,
                "account_name": line.account.account_name,
                "description": line.journal_entry.description,
                "debit": line.debit,
                "credit": line.credit,
                "running_balance": running_balance,
            }
        )

    summary = {
        "account_id": account_id,
        "account_name": (
            lines[0].account.account_name
            if lines
            else ""
        ),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "closing_balance": running_balance,
    }

    return {
        "ledger": ledger,
        "summary": summary,
    }
