from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.accounts_receivable import AccountsReceivable
from app.models.customer import Customer
from app.models.sales_invoice import SalesInvoice

from app.modules.accounts_receivable.schemas import (
    AccountsReceivableCreate,
)
def create_accounts_receivable(
    db: Session,
    receivable: AccountsReceivableCreate,
):
    invoice = (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.id == receivable.sales_invoice_id
        )
        .first()
    )

    if not invoice:
        raise ValueError("Sales Invoice not found.")

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == receivable.customer_id
        )
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    ar = AccountsReceivable(
        customer_id=receivable.customer_id,
        sales_invoice_id=receivable.sales_invoice_id,
        company_id=receivable.company_id,
        branch_id=receivable.branch_id,
        invoice_amount=invoice.total_amount,
        paid_amount=invoice.paid_amount,
        balance_amount=invoice.balance_amount,
    )

    db.add(ar)
    db.commit()
    db.refresh(ar)

    return ar
def get_accounts_receivables(db: Session):
    return db.query(AccountsReceivable).all()


def get_accounts_receivable(
    db: Session,
    receivable_id: UUID,
):
    return (
        db.query(AccountsReceivable)
        .filter(
            AccountsReceivable.id == receivable_id
        )
        .first()
    )


def get_customer_receivables(
    db: Session,
    customer_id: UUID,
):
    return (
        db.query(AccountsReceivable)
        .filter(
            AccountsReceivable.customer_id == customer_id
        )
        .all()
    )
def sync_receivable(
    db: Session,
    sales_invoice_id: UUID,
):
    receivable = (
        db.query(AccountsReceivable)
        .filter(
            AccountsReceivable.sales_invoice_id
            == sales_invoice_id
        )
        .first()
    )

    if not receivable:
        return

    invoice = (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.id == sales_invoice_id
        )
        .first()
    )

    receivable.invoice_amount = invoice.total_amount
    receivable.paid_amount = invoice.paid_amount
    receivable.balance_amount = invoice.balance_amount

    db.commit()
def delete_accounts_receivable(
    db: Session,
    receivable_id: UUID,
    ):
     receivable = get_accounts_receivable(
        db,
        receivable_id,
    )

     if not receivable:
        return False

     db.delete(receivable)
     db.commit()

     return True