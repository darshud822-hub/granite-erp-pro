from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TrialBalanceItem(BaseModel):
    account_id: UUID
    account_code: str
    account_name: str

    debit: Decimal
    credit: Decimal


class TrialBalanceResponse(BaseModel):
    accounts: list[TrialBalanceItem]

    total_debit: Decimal
    total_credit: Decimal

    is_balanced: bool