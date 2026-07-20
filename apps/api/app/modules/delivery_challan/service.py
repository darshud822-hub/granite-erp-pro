from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.delivery_challan import (
    DeliveryChallan,
    DeliveryStatus,
)
from app.models.delivery_challan_item import DeliveryChallanItem
from app.models.sales_order import (
    SalesOrder,
    SalesOrderStatus,
)
from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.modules.delivery_challan.schemas import (
    DeliveryChallanCreate,
)
from enum import Enum

class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"
    TRANSFER = "TRANSFER"

movement_type: Mapped[MovementType]
def create_delivery_challan(
    db: Session,
    challan: DeliveryChallanCreate,
):
    # Validate Sales Order
    sales_order = (
        db.query(SalesOrder)
        .filter(
            SalesOrder.id == challan.sales_order_id
        )
        .first()
    )

    if not sales_order:
        raise ValueError("Sales Order not found.")

    if sales_order.status == SalesOrderStatus.DELIVERED:
        raise ValueError("Sales Order already delivered.")

    customer = (
        db.query(Customer)
        .filter(Customer.id == challan.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    delivery = DeliveryChallan(
        challan_number=challan.challan_number,
        challan_date=challan.challan_date,
        sales_order_id=challan.sales_order_id,
        customer_id=challan.customer_id,
        company_id=challan.company_id,
        branch_id=challan.branch_id,
        remarks=challan.remarks,
    )

    db.add(delivery)
    db.flush()

    for item in challan.items:

        stock = (
            db.query(Stock)
            .filter(
                Stock.product_id == item.product_id,
                Stock.warehouse_id == item.warehouse_id,
                Stock.company_id == challan.company_id,
                Stock.branch_id == challan.branch_id,
            )
            .first()
        )

        if not stock:
            raise ValueError(
                "Stock record not found."
            )

        if stock.quantity < item.quantity:
            raise ValueError(
                "Insufficient stock."
            )

        # Physical stock deduction
        stock.quantity -= item.quantity

        # Release reserved quantity
        stock.reserved_quantity -= item.quantity

        # Recalculate available stock
        stock.available_quantity = (
            stock.quantity
            - stock.reserved_quantity
        )

        delivery_item = DeliveryChallanItem(
            delivery_challan_id=delivery.id,
            product_id=item.product_id,
            warehouse_id=item.warehouse_id,
            quantity=item.quantity,
        )

        db.add(delivery_item)

        movement = StockMovement(
    movement_no=f"SM-{challan.challan_number}",
    movement_type="OUT",
    product_id=item.product_id,
    warehouse_id=item.warehouse_id,
    company_id=challan.company_id,
    branch_id=challan.branch_id,
    quantity=item.quantity,
    remarks=f"Delivery Challan {challan.challan_number}",
)

        db.add(movement)

    sales_order.status = SalesOrderStatus.DELIVERED
    delivery.status = DeliveryStatus.DELIVERED

    db.commit()
    db.refresh(delivery)

    return delivery

def get_delivery_challans(db: Session):
    return db.query(DeliveryChallan).all()


def get_delivery_challan(
    db: Session,
    challan_id,
):
    return (
        db.query(DeliveryChallan)
        .filter(
            DeliveryChallan.id == challan_id
        )
        .first()
    )


def delete_delivery_challan(
    db: Session,
    challan_id,
):
    challan = get_delivery_challan(
        db,
        challan_id,
    )

    if not challan:
        return False

    db.delete(challan)
    db.commit()

    return True