from decimal import Decimal
from sqlalchemy import String

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class JournalEntryLine(BaseModel):
    __tablename__ = "journal_entry_lines"

    journal_entry_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_entries.id"),
        nullable=False,
    )

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("chart_of_accounts.id"),
        nullable=False,
    )

    debit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    credit: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    narration: Mapped[str | None] = mapped_column(
    String(300),
    nullable=True,
)

    journal_entry = relationship(
        "JournalEntry",
        back_populates="lines",
    )

    account = relationship("ChartOfAccount")