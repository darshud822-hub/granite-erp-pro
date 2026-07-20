from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.grn import GRN
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_item import PurchaseInvoiceItem
from app.models.supplier import Supplier
from app.modules.purchase_invoice.schemas import PurchaseInvoiceCreate


def create_purchase_invoice(
    db: Session,
    invoice: PurchaseInvoiceCreate,
):
    # Validate Supplier
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == invoice.supplier_id)
        .first()
    )

    if not supplier:
        raise ValueError("Supplier not found.")

    # Validate GRN
    grn = (
        db.query(GRN)
        .filter(GRN.id == invoice.grn_id)
        .first()
    )

    if not grn:
        raise ValueError("GRN not found.")

    # Prevent duplicate invoice numbers
    existing = (
        db.query(PurchaseInvoice)
        .filter(
            PurchaseInvoice.invoice_number == invoice.invoice_number
        )
        .first()
    )

    if existing:
        raise ValueError("Invoice number already exists.")

    subtotal = Decimal("0")
    tax_amount = Decimal("0")

    # Calculate totals
    for item in invoice.items:
        line_subtotal = item.quantity * item.unit_price
        line_tax = (
            line_subtotal * item.tax_percent
        ) / Decimal("100")

        subtotal += line_subtotal
        tax_amount += line_tax

    grand_total = (
        subtotal
        + tax_amount
        - invoice.discount_amount
    )

    db_invoice = PurchaseInvoice(
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date,
        supplier_id=invoice.supplier_id,
        grn_id=invoice.grn_id,
        company_id=invoice.company_id,
        branch_id=invoice.branch_id,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=invoice.discount_amount,
        grand_total=grand_total,
        remarks=invoice.remarks,
    )

    db.add(db_invoice)
    db.flush()

    # Save Invoice Items
    for item in invoice.items:

        line_subtotal = item.quantity * item.unit_price
        line_tax = (
            line_subtotal * item.tax_percent
        ) / Decimal("100")

        line_total = line_subtotal + line_tax

        db_item = PurchaseInvoiceItem(
            purchase_invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_percent=item.tax_percent,
            line_total=line_total,
        )

        db.add(db_item)

    # Update Supplier Outstanding Balance
    supplier.outstanding_balance += grand_total

    db.commit()
    db.refresh(db_invoice)

    return db_invoice


def get_purchase_invoices(db: Session):
    return db.query(PurchaseInvoice).all()


def get_purchase_invoice(
    db: Session,
    invoice_id,
):
    return (
        db.query(PurchaseInvoice)
        .filter(
            PurchaseInvoice.id == invoice_id
        )
        .first()
    )


def delete_purchase_invoice(
    db: Session,
    invoice_id,
):
    invoice = get_purchase_invoice(
        db,
        invoice_id,
    )

    if not invoice:
        return False

    db.delete(invoice)
    db.commit()

    return True