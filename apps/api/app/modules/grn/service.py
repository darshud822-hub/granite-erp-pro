from sqlalchemy.orm import Session

from app.models.grn import GRN
from app.models.grn_item import GRNItem
from app.models.purchase_order import PurchaseOrder
from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.modules.grn.schemas import GRNCreate


def create_grn(
    db: Session,
    grn: GRNCreate,
):
    purchase_order = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == grn.purchase_order_id
        )
        .first()
    )

    if not purchase_order:
        raise ValueError("Purchase Order not found.")

    existing = (
        db.query(GRN)
        .filter(
            GRN.grn_number == grn.grn_number
        )
        .first()
    )

    if existing:
        raise ValueError("GRN number already exists.")

    db_grn = GRN(
        grn_number=grn.grn_number,
        grn_date=grn.grn_date,
        purchase_order_id=grn.purchase_order_id,
        warehouse_id=grn.warehouse_id,
        company_id=grn.company_id,
        branch_id=grn.branch_id,
        remarks=grn.remarks,
    )

    db.add(db_grn)
    db.flush()

    for item in grn.items:

        db_item = GRNItem(
            grn_id=db_grn.id,
            product_id=item.product_id,
            received_quantity=item.received_quantity,
        )

        db.add(db_item)

        stock = (
            db.query(Stock)
            .filter(
                Stock.product_id == item.product_id,
                Stock.warehouse_id == grn.warehouse_id,
            )
            .first()
        )

        if not stock:
         stock = Stock(
        product_id=item.product_id,
        warehouse_id=grn.warehouse_id,
        company_id=grn.company_id,
        branch_id=grn.branch_id,
        quantity=0,
        reserved_quantity=0,
        available_quantity=0,
    )
    db.add(stock)
    db.flush()

    stock.quantity += item.received_quantity
    stock.available_quantity = (
    stock.quantity - stock.reserved_quantity
)

    movement = StockMovement(
            movement_no=f"GRN-{db_grn.grn_number}-{item.product_id}",
            movement_type="PURCHASE",
            product_id=item.product_id,
            warehouse_id=grn.warehouse_id,
            company_id=grn.company_id,
            branch_id=grn.branch_id,
            quantity=item.received_quantity,
            remarks=f"Received via {grn.grn_number}",
        )

    db.add(movement)

    db.commit()
    db.refresh(db_grn)

    return db_grn


def get_grns(db: Session):
    return db.query(GRN).all()


def get_grn(
    db: Session,
    grn_id,
):
    return (
        db.query(GRN)
        .filter(
            GRN.id == grn_id
        )
        .first()
    )


def delete_grn(
    db: Session,
    grn_id,
):
    grn = get_grn(db, grn_id)

    if not grn:
        return False

    db.delete(grn)
    db.commit()

    return True