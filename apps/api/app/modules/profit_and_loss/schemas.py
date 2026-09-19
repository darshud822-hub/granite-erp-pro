from decimal import Decimal

from pydantic import BaseModel


class ProfitLossItem(BaseModel):
    account_code: str
    account_name: str
    amount: Decimal


class ProfitLossResponse(BaseModel):
    revenue: list[ProfitLossItem]
    expenses: list[ProfitLossItem]

    total_revenue: Decimal
    total_expenses: Decimal

    net_profit: Decimal