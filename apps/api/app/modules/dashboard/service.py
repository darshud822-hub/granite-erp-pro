from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.employee import Employee
from app.models.sales_invoice import SalesInvoice
from app.models.purchase_invoice import PurchaseInvoice
from app.models.accounts_receivable import AccountsReceivable
from app.models.accounts_payable import AccountsPayable
from app.models.stock import Stock
from sqlalchemy import extract
from calendar import month_abbr


def get_dashboard(db: Session):

    total_customers = db.query(Customer).count()
    total_suppliers = db.query(Supplier).count()
    total_products = db.query(Product).count()
    total_employees = db.query(Employee).count()

    total_sales = (
        db.query(
            func.coalesce(func.sum(SalesInvoice.total_amount), 0)
        ).scalar()
    )

    total_purchases = (
        db.query(
            func.coalesce(func.sum(PurchaseInvoice.grand_total), 0)
        ).scalar()
    )

    accounts_receivable = (
        db.query(
            func.coalesce(
                func.sum(AccountsReceivable.balance_amount),
                0,
            )
        ).scalar()
    )

    accounts_payable = (
        db.query(
            func.coalesce(
                func.sum(AccountsPayable.balance_amount),
                0,
            )
        ).scalar()
    )

    inventory_value = (
        db.query(
            func.coalesce(
                func.sum(Stock.quantity * Stock.unit_cost),
                0,
            )
        ).scalar()
    )

    net_profit = total_sales - total_purchases

    current_year = 2026

    monthly_sales = []

    for month in range(1, 13):

     sales = (
        db.query(
            func.coalesce(
                func.sum(SalesInvoice.total_amount),
                0,
            )
        )
        .filter(
            extract("year", SalesInvoice.invoice_date) == current_year
        )
        .filter(
            extract("month", SalesInvoice.invoice_date) == month
        )
        .scalar()
    )

    purchases = (
        db.query(
            func.coalesce(
                func.sum(PurchaseInvoice.grand_total),
                0,
            )
        )
        .filter(
            extract("year", PurchaseInvoice.invoice_date) == current_year
        )
        .filter(
            extract("month", PurchaseInvoice.invoice_date) == month
        )
        .scalar()
    )

    monthly_sales.append(
    {
        "month": month_abbr[month],
        "sales": Decimal(sales),
        "purchases": Decimal(purchases),
        "profit": Decimal(sales) - Decimal(purchases),
    }
)

    # Recent Sales
    recent_sales = (
        db.query(SalesInvoice)
        .order_by(SalesInvoice.invoice_date.desc())
        .limit(5)
        .all()
    )

    recent_sales_data = [
        {
            "invoice": sale.invoice_number,
            "customer": sale.customer.company_name,
            "date": sale.invoice_date.strftime("%d-%m-%Y"),
            "amount": Decimal(sale.total_amount),
            "status": sale.status.value,
        }
        for sale in recent_sales
    ]

    # Low Stock
    low_stock = (
        db.query(Stock)
        .filter(
            Stock.available_quantity <= Stock.minimum_stock
        )
        .order_by(Stock.available_quantity.asc())
        .limit(5)
        .all()
    )

    low_stock_data = [
        {
            "product": item.product.product_name,
            "available": Decimal(item.available_quantity),
            "minimum": Decimal(item.minimum_stock),
        }
        for item in low_stock
    ]
    activities = [
    {
        "icon": "invoice",
        "title": "Sales Invoice Created",
        "description": "Invoice INV-1025",
        "time": "10 min ago",
    },
    {
        "icon": "customer",
        "title": "New Customer",
        "description": "ABC Granite Pvt Ltd",
        "time": "35 min ago",
    },
    {
        "icon": "purchase",
        "title": "Purchase Invoice",
        "description": "Supplier payment updated",
        "time": "1 hour ago",
    },
]
    notifications = [
    {"message": "5 Products are below minimum stock"},
    {"message": "3 Customer payments are overdue"},
    {"message": "2 Purchase Orders pending approval"},
]

    return {
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_products": total_products,
        "total_employees": total_employees,

        "total_sales": Decimal(total_sales),
        "total_purchases": Decimal(total_purchases),

        "accounts_receivable": Decimal(accounts_receivable),
        "accounts_payable": Decimal(accounts_payable),

        "net_profit": Decimal(net_profit),
        "inventory_value": Decimal(inventory_value),

        "monthly_sales": monthly_sales,
        "recent_sales": recent_sales_data,
        "low_stock": low_stock_data,
        "activities": activities,
        "notifications": notifications,
    }