from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.accounts_payable import AccountsPayable
from app.models.purchase_invoice import (
    PurchaseInvoice,
    PurchaseInvoiceStatus,
)
from app.models.supplier import Supplier

from app.modules.accounts_payable.schemas import (
    AccountsPayableCreate,
)
def create_accounts_payable(
    db: Session,
    payable: AccountsPayableCreate,
):
    invoice = (
        db.query(PurchaseInvoice)
        .filter(
            PurchaseInvoice.id == payable.purchase_invoice_id
        )
        .first()
    )

    if not invoice:
        raise ValueError("Purchase Invoice not found.")

    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == payable.supplier_id
        )
        .first()
    )

    if not supplier:
        raise ValueError("Supplier not found.")

    ap = AccountsPayable(
        supplier_id=payable.supplier_id,
        purchase_invoice_id=payable.purchase_invoice_id,
        company_id=payable.company_id,
        branch_id=payable.branch_id,
        invoice_amount=invoice.total_amount,
        paid_amount=invoice.paid_amount,
        balance_amount=invoice.balance_amount,
    )

    db.add(ap)
    db.commit()
    db.refresh(ap)

    return ap
def get_accounts_payables(db: Session):
    return db.query(AccountsPayable).all()


def get_accounts_payable(
    db: Session,
    payable_id: UUID,
):
    return (
        db.query(AccountsPayable)
        .filter(
            AccountsPayable.id == payable_id
        )
        .first()
    )


def get_supplier_payables(
    db: Session,
    supplier_id: UUID,
):
    return (
        db.query(AccountsPayable)
        .filter(
            AccountsPayable.supplier_id == supplier_id
        )
        .all()
    )
def sync_payable(
    db: Session,
    purchase_invoice_id: UUID,
):
    payable = (
        db.query(AccountsPayable)
        .filter(
            AccountsPayable.purchase_invoice_id
            == purchase_invoice_id
        )
        .first()
    )

    if not payable:
        return

    invoice = (
        db.query(PurchaseInvoice)
        .filter(
            PurchaseInvoice.id == purchase_invoice_id
        )
        .first()
    )

    payable.invoice_amount = invoice.total_amount
    payable.paid_amount = invoice.paid_amount
    payable.balance_amount = invoice.balance_amount

    db.commit()
def delete_accounts_payable(
    db: Session,
    payable_id: UUID,
):
    payable = get_accounts_payable(
        db,
        payable_id,
    )

    if not payable:
        return False

    db.delete(payable)
    db.commit()

    return True