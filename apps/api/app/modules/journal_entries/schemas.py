from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.journal_entry import JournalStatus


class JournalEntryLineCreate(BaseModel):
    account_id: UUID
    debit: Decimal = Decimal("0")
    credit: Decimal = Decimal("0")
    narration: str | None = None


class JournalEntryLineResponse(JournalEntryLineCreate):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class JournalEntryCreate(BaseModel):
    reference_number: str | None = None
    description: str | None = None

    company_id: UUID
    branch_id: UUID

    lines: list[JournalEntryLineCreate]


class JournalEntryResponse(BaseModel):
    id: UUID

    journal_number: str

    reference_number: str | None = None
    description: str | None = None

    status: JournalStatus

    company_id: UUID
    branch_id: UUID

    lines: list[JournalEntryLineResponse]

    model_config = ConfigDict(
        from_attributes=True
    )