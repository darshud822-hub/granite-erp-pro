from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class AccountType(str, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class ChartOfAccount(BaseModel):
    __tablename__ = "chart_of_accounts"

    account_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    account_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    account_type: Mapped[AccountType] = mapped_column(
        SqlEnum(AccountType),
        nullable=False,
    )

    parent_account_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("chart_of_accounts.id"),
        nullable=True,
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    parent = relationship(
        "ChartOfAccount",
        remote_side="ChartOfAccount.id",
        backref="children",
    )

    company = relationship("Company")
    branch = relationship("Branch")