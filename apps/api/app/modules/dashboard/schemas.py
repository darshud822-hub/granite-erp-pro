from decimal import Decimal
from pydantic import BaseModel


class MonthlySales(BaseModel):
    month: str
    sales: Decimal
    purchases: Decimal
    profit: Decimal


class RecentSale(BaseModel):
    invoice: str
    customer: str
    date: str
    amount: Decimal
    status: str

class LowStockItem(BaseModel):
    product: str
    available: Decimal
    minimum: Decimal

class Activity(BaseModel):
    icon: str
    title: str
    description: str
    time: str


class DashboardResponse(BaseModel):
    total_customers: int
    total_suppliers: int
    total_products: int
    total_employees: int

    total_sales: Decimal
    total_purchases: Decimal

    accounts_receivable: Decimal
    accounts_payable: Decimal

    net_profit: Decimal
    inventory_value: Decimal

    monthly_sales: list[MonthlySales]
    recent_sales: list[RecentSale]

    low_stock: list[LowStockItem]
    activities: list[Activity]