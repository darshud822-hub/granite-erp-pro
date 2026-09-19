from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.chart_of_account import ChartOfAccount
from app.models.journal_entry import (
    JournalEntry,
    JournalStatus,
)
from app.models.journal_entry_line import JournalEntryLine

from app.modules.journal_entries.schemas import (
    JournalEntryCreate,
)
def generate_journal_number(db: Session) -> str:
    count = db.query(JournalEntry).count() + 1
    return f"JE-{count:06d}"
def create_journal_entry(
    db: Session,
    data: JournalEntryCreate,
):
    total_debit = Decimal("0")
    total_credit = Decimal("0")

    # Validate accounts and calculate totals
    for line in data.lines:

        account = (
            db.query(ChartOfAccount)
            .filter(
                ChartOfAccount.id == line.account_id
            )
            .first()
        )

        if not account:
            raise ValueError("Chart of Account not found.")

        total_debit += line.debit
        total_credit += line.credit

    if total_debit != total_credit:
        raise ValueError(
            "Total Debit must equal Total Credit."
        )

    journal = JournalEntry(
        journal_number=generate_journal_number(db),
        reference_number=data.reference_number,
        description=data.description,
        status=JournalStatus.DRAFT,
        company_id=data.company_id,
        branch_id=data.branch_id,
    )

    db.add(journal)
    db.flush()

    for line in data.lines:
        journal_line = JournalEntryLine(
            journal_entry_id=journal.id,
            account_id=line.account_id,
            debit=line.debit,
            credit=line.credit,
            narration=line.narration,
        )

        db.add(journal_line)

    db.commit()
    db.refresh(journal)

    return journal
from uuid import UUID


def get_journal_entries(db: Session):
    return (
        db.query(JournalEntry)
        .all()
    )


def get_journal_entry(
    db: Session,
    journal_id: UUID,
):
    return (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == journal_id
        )
        .first()
    )
def post_journal(
    db: Session,
    journal_id: UUID,
):
    journal = get_journal_entry(
        db,
        journal_id,
    )

    if not journal:
        return None

    journal.status = JournalStatus.POSTED

    db.commit()
    db.refresh(journal)

    return journal
def delete_journal(
    db: Session,
    journal_id: UUID,
):
    journal = get_journal_entry(
        db,
        journal_id,
    )

    if not journal:
        return False

    if journal.status == JournalStatus.POSTED:
        raise ValueError(
            "Posted journals cannot be deleted."
        )

    db.delete(journal)
    db.commit()

    return True