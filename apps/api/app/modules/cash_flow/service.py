from decimal import Decimal

from sqlalchemy.orm import Session, joinedload

from app.models.chart_of_account import CashFlowCategory
from app.models.journal_entry import JournalEntry, JournalStatus
from app.models.journal_entry_line import JournalEntryLine


def get_cash_flow(db: Session):
    lines = (
        db.query(JournalEntryLine)
        .join(JournalEntry)
        .options(
            joinedload(JournalEntryLine.account)
        )
        .filter(
            JournalEntry.status == JournalStatus.POSTED
        )
        .all()
    )

    operating = {}
    investing = {}
    financing = {}

    operating_total = Decimal("0")
    investing_total = Decimal("0")
    financing_total = Decimal("0")

    for line in lines:

        account = line.account

        if account.cash_flow_category is None:
            continue

        amount = line.debit - line.credit

        if account.cash_flow_category == CashFlowCategory.OPERATING:

            if account.id not in operating:
                operating[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            operating[account.id]["amount"] += amount
            operating_total += amount

        elif account.cash_flow_category == CashFlowCategory.INVESTING:

            if account.id not in investing:
                investing[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            investing[account.id]["amount"] += amount
            investing_total += amount

        elif account.cash_flow_category == CashFlowCategory.FINANCING:

            if account.id not in financing:
                financing[account.id] = {
                    "account_code": account.account_code,
                    "account_name": account.account_name,
                    "amount": Decimal("0"),
                }

            financing[account.id]["amount"] += amount
            financing_total += amount

    return {
        "operating_activities": list(operating.values()),
        "investing_activities": list(investing.values()),
        "financing_activities": list(financing.values()),
        "net_cash_from_operating": operating_total,
        "net_cash_from_investing": investing_total,
        "net_cash_from_financing": financing_total,
        "net_cash_flow": (
            operating_total
            + investing_total
            + financing_total
        ),
    }