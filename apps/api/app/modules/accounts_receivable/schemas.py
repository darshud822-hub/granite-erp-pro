from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccountsReceivableBase(BaseModel):
    customer_id: UUID
    sales_invoice_id: UUID

    company_id: UUID
    branch_id: UUID

    invoice_amount: Decimal
    paid_amount: Decimal = Decimal("0")
    balance_amount: Decimal = Decimal("0")


class AccountsReceivableCreate(AccountsReceivableBase):
    pass


class AccountsReceivableUpdate(BaseModel):
    paid_amount: Decimal | None = None
    balance_amount: Decimal | None = None


class AccountsReceivableResponse(AccountsReceivableBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )