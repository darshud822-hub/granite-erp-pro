from sqlalchemy.orm import Session

from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.modules.purchase_order.schemas import (
    PurchaseOrderCreate,
)


def create_purchase_order(
    db: Session,
    purchase_order: PurchaseOrderCreate,
):
    existing = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.po_number == purchase_order.po_number
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Purchase Order number already exists."
        )

    db_po = PurchaseOrder(
        po_number=purchase_order.po_number,
        po_date=purchase_order.po_date,
        supplier_id=purchase_order.supplier_id,
        company_id=purchase_order.company_id,
        branch_id=purchase_order.branch_id,
        status=purchase_order.status,
        remarks=purchase_order.remarks,
    )

    db.add(db_po)
    db.flush()   # Generates the Purchase Order ID

    for item in purchase_order.items:
        db_item = PurchaseOrderItem(
            purchase_order_id=db_po.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_percent=item.tax_percent,
        )

        db.add(db_item)

    db.commit()
    db.refresh(db_po)

    return db_po


def get_purchase_orders(db: Session):
    return db.query(PurchaseOrder).all()


def get_purchase_order(
    db: Session,
    purchase_order_id,
):
    return (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == purchase_order_id
        )
        .first()
    )


def delete_purchase_order(
    db: Session,
    purchase_order_id,
):
    purchase_order = get_purchase_order(
        db,
        purchase_order_id,
    )

    if not purchase_order:
        return False

    db.delete(purchase_order)
    db.commit()

    return True