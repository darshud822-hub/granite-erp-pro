from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.purchase_invoice import (
    PurchaseInvoice,
    PurchaseInvoiceStatus,
)
from app.models.supplier import Supplier
from app.models.supplier_payment import (
    SupplierPayment,
    SupplierPaymentStatus,
)

from app.modules.supplier_payment.schemas import (
    SupplierPaymentCreate,
)
def create_supplier_payment(
    db: Session,
    payment: SupplierPaymentCreate,
):
    invoice = (
        db.query(PurchaseInvoice)
        .filter(
            PurchaseInvoice.id == payment.purchase_invoice_id
        )
        .first()
    )

    if not invoice:
        raise ValueError("Purchase Invoice not found.")

    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == payment.supplier_id
        )
        .first()
    )

    if not supplier:
        raise ValueError("Supplier not found.")

    if payment.amount <= 0:
        raise ValueError(
            "Payment amount must be greater than zero."
        )

    if payment.amount > invoice.balance_amount:
        raise ValueError(
            "Payment exceeds outstanding balance."
        )

    supplier_payment = SupplierPayment(
        payment_number=payment.payment_number,
        payment_date=payment.payment_date,
        purchase_invoice_id=payment.purchase_invoice_id,
        supplier_id=payment.supplier_id,
        company_id=payment.company_id,
        branch_id=payment.branch_id,
        payment_method=payment.payment_method,
        amount=payment.amount,
        reference_number=payment.reference_number,
        remarks=payment.remarks,
        status=SupplierPaymentStatus.COMPLETED,
    )

    db.add(supplier_payment)

    invoice.paid_amount += payment.amount
    invoice.balance_amount -= payment.amount

    if invoice.balance_amount == Decimal("0"):
        invoice.status = PurchaseInvoiceStatus.PAID
    else:
        invoice.status = (
            PurchaseInvoiceStatus.PARTIALLY_PAID
        )

    db.commit()
    db.refresh(supplier_payment)

    return supplier_payment
def get_supplier_payments(db: Session):
    return db.query(SupplierPayment).all()


def get_supplier_payment(
    db: Session,
    payment_id,
):
    return (
        db.query(SupplierPayment)
        .filter(
            SupplierPayment.id == payment_id
        )
        .first()
    )


def delete_supplier_payment(
    db: Session,
    payment_id,
):
    payment = get_supplier_payment(
        db,
        payment_id,
    )

    if not payment:
        return False

    db.delete(payment)
    db.commit()

    return True