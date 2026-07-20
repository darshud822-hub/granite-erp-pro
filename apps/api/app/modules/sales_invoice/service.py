from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.delivery_challan import DeliveryChallan
from app.models.sales_invoice import (
    SalesInvoice,
    SalesInvoiceStatus,
)
from app.models.sales_invoice_item import SalesInvoiceItem

from app.modules.sales_invoice.schemas import (
    SalesInvoiceCreate,
)
def create_sales_invoice(
    db: Session,
    invoice: SalesInvoiceCreate,
):
    delivery = (
        db.query(DeliveryChallan)
        .filter(
            DeliveryChallan.id == invoice.delivery_challan_id
        )
        .first()
    )

    if not delivery:
        raise ValueError("Delivery Challan not found.")

    customer = (
        db.query(Customer)
        .filter(Customer.id == invoice.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    subtotal = Decimal("0")
    tax_amount = Decimal("0")
    grand_total = Decimal("0")

    db_invoice = SalesInvoice(
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date,
        delivery_challan_id=invoice.delivery_challan_id,
        customer_id=invoice.customer_id,
        company_id=invoice.company_id,
        branch_id=invoice.branch_id,
        remarks=invoice.remarks,
    )

    db.add(db_invoice)
    db.flush()

    for item in invoice.items:

        line_subtotal = item.quantity * item.unit_price

        taxable = line_subtotal - item.discount

        line_tax = (
            taxable * item.tax_percent
        ) / Decimal("100")

        line_total = taxable + line_tax

        subtotal += taxable
        tax_amount += line_tax
        grand_total += line_total

        db_item = SalesInvoiceItem(
            sales_invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount,
            tax_percent=item.tax_percent,
            line_total=line_total,
        )

        db.add(db_item)

    db_invoice.subtotal = subtotal
    db_invoice.tax_amount = tax_amount
    db_invoice.total_amount = grand_total
    db_invoice.status = SalesInvoiceStatus.DRAFT

    db.commit()
    db.refresh(db_invoice)

    return db_invoice
def get_sales_invoices(db: Session):
    return db.query(SalesInvoice).all()


def get_sales_invoice(
    db: Session,
    invoice_id,
):
    return (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.id == invoice_id
        )
        .first()
    )


def delete_sales_invoice(
    db: Session,
    invoice_id,
):
    invoice = get_sales_invoice(
        db,
        invoice_id,
    )

    if not invoice:
        return False

    db.delete(invoice)
    db.commit()

    return True