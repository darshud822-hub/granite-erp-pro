from decimal import Decimal

from pydantic import BaseModel


class CashFlowItem(BaseModel):
    account_code: str
    account_name: str
    amount: Decimal


class CashFlowResponse(BaseModel):
    operating_activities: list[CashFlowItem]
    investing_activities: list[CashFlowItem]
    financing_activities: list[CashFlowItem]

    net_cash_from_operating: Decimal
    net_cash_from_investing: Decimal
    net_cash_from_financing: Decimal

    net_cash_flow: Decimal