from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccountsPayableBase(BaseModel):
    supplier_id: UUID
    purchase_invoice_id: UUID

    company_id: UUID
    branch_id: UUID

    invoice_amount: Decimal
    paid_amount: Decimal = Decimal("0")
    balance_amount: Decimal = Decimal("0")


class AccountsPayableCreate(AccountsPayableBase):
    pass


class AccountsPayableUpdate(BaseModel):
    paid_amount: Decimal | None = None
    balance_amount: Decimal | None = None


class AccountsPayableResponse(AccountsPayableBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )