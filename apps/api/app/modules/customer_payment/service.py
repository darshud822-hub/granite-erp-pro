from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_payment import (
    CustomerPayment,
    CustomerPaymentStatus,
)
from app.models.sales_invoice import (
    SalesInvoice,
    SalesInvoiceStatus,
)

from app.modules.customer_payment.schemas import (
    CustomerPaymentCreate,
)
def create_customer_payment(
    db: Session,
    payment: CustomerPaymentCreate,
):
    invoice = (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.id == payment.sales_invoice_id
        )
        .first()
    )

    if not invoice:
        raise ValueError("Sales Invoice not found.")

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == payment.customer_id
        )
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    if payment.amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    if payment.amount > invoice.balance_amount:
        raise ValueError("Payment exceeds outstanding balance.")

    customer_payment = CustomerPayment(
        payment_number=payment.payment_number,
        payment_date=payment.payment_date,
        sales_invoice_id=payment.sales_invoice_id,
        customer_id=payment.customer_id,
        company_id=payment.company_id,
        branch_id=payment.branch_id,
        payment_method=payment.payment_method,
        amount=payment.amount,
        reference_number=payment.reference_number,
        remarks=payment.remarks,
        status=CustomerPaymentStatus.COMPLETED,
    )

    db.add(customer_payment)

    invoice.paid_amount += payment.amount
    invoice.balance_amount -= payment.amount

    if invoice.balance_amount == Decimal("0"):
        invoice.status = SalesInvoiceStatus.PAID
    else:
        invoice.status = SalesInvoiceStatus.PARTIALLY_PAID

    db.commit()
    db.refresh(customer_payment)

    return customer_payment
def get_customer_payments(db: Session):
    return db.query(CustomerPayment).all()


def get_customer_payment(
    db: Session,
    payment_id,
):
    return (
        db.query(CustomerPayment)
        .filter(
            CustomerPayment.id == payment_id
        )
        .first()
    )


def delete_customer_payment(
    db: Session,
    payment_id,
):
    payment = get_customer_payment(
        db,
        payment_id,
    )

    if not payment:
        return False

    db.delete(payment)
    db.commit()

    return True