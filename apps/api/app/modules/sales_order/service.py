from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.sales_order import SalesOrder
from app.models.sales_order_item import SalesOrderItem
from app.models.stock import Stock
from app.modules.sales_order.schemas import SalesOrderCreate


def create_sales_order(
    db: Session,
    order: SalesOrderCreate,
):
    # Validate Customer
    customer = (
        db.query(Customer)
        .filter(Customer.id == order.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    total_amount = Decimal("0")

    db_order = SalesOrder(
        order_number=order.order_number,
        order_date=order.order_date,
        customer_id=order.customer_id,
        company_id=order.company_id,
        branch_id=order.branch_id,
        remarks=order.remarks,
    )

    db.add(db_order)
    db.flush()

    for item in order.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise ValueError("Product not found.")

        stock = (
            db.query(Stock)
            .filter(
                Stock.product_id == item.product_id,
                Stock.company_id == order.company_id,
                Stock.branch_id == order.branch_id,
            )
            .first()
        )

        if not stock:
            raise ValueError(
                f"No stock available for {product.name}"
            )

        if stock.available_quantity < item.quantity:
            raise ValueError(
                f"Insufficient stock for {product.name}"
            )

        # Reserve Stock
        stock.reserved_quantity += item.quantity
        stock.available_quantity -= item.quantity

        subtotal = item.quantity * item.unit_price
        discount = item.discount
        taxable = subtotal - discount

        tax = (
            taxable * item.tax_percent
        ) / Decimal("100")

        line_total = taxable + tax

        total_amount += line_total

        db_item = SalesOrderItem(
            sales_order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount,
            tax_percent=item.tax_percent,
            line_total=line_total,
        )

        db.add(db_item)

    db_order.total_amount = total_amount

    db.commit()
    db.refresh(db_order)

    return db_order