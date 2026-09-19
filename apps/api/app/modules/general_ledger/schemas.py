from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class LedgerEntryResponse(BaseModel):
    journal_number: str
    transaction_date: datetime

    account_id: UUID
    account_name: str

    description: str | None = None

    debit: Decimal
    credit: Decimal

    running_balance: Decimal


class LedgerSummaryResponse(BaseModel):
    account_id: UUID
    account_name: str

    total_debit: Decimal
    total_credit: Decimal

    closing_balance: Decimal