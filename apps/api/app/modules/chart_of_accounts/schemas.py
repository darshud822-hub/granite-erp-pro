from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.chart_of_account import AccountType


class ChartOfAccountBase(BaseModel):
    account_code: str
    account_name: str
    account_type: AccountType

    parent_account_id: UUID | None = None

    company_id: UUID
    branch_id: UUID

    is_active: bool = True


class ChartOfAccountCreate(ChartOfAccountBase):
    pass


class ChartOfAccountUpdate(BaseModel):
    account_code: str | None = None
    account_name: str | None = None
    account_type: AccountType | None = None

    parent_account_id: UUID | None = None

    is_active: bool | None = None


class ChartOfAccountResponse(ChartOfAccountBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )