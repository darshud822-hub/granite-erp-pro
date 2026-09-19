from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.company.router import router as company_router
from app.modules.branch.router import router as branch_router 
from app.modules.employee.router import router as employee_router
from app.modules.customer.router import router as customer_router
from app.modules.department.router import router as department_router
from app.modules.designation.router import router as designation_router
from app.modules.supplier.router import router as supplier_router
from app.modules.product_category.router import (
    router as product_category_router,
)
from app.modules.uom.router import router as uom_router
from app.modules.product.router import router as product_router
from app.modules.warehouse.router import router as warehouse_router
from app.modules.stock.router import router as stock_router
from app.modules.stock_movement.router import router as stock_movement_router
from app.modules.purchase_order.router import router as purchase_order_router
from app.modules.grn.router import router as grn_router
from app.modules.purchase_invoice.router import router as purchase_invoice_router
from app.modules.delivery_challan.router import (
    router as delivery_challan_router,
)
from app.modules.sales_invoice.router import (
    router as sales_invoice_router,
)
from app.modules.customer_payment.router import router as customer_payment_router
from app.modules.supplier_payment.router import (
    router as supplier_payment_router,
)
from app.modules.accounts_receivable.router import (
    router as accounts_receivable_router,
)
from app.modules.accounts_payable.router import (
    router as accounts_payable_router,
)
from app.modules.chart_of_accounts.router import (
    router as chart_of_accounts_router,
)
from app.modules.journal_entries.router import (
    router as journal_entries_router,
)
from app.modules.general_ledger.router import (
    router as general_ledger_router,
)
from app.modules.trial_balance.router import (
    router as trial_balance_router,
)
from app.modules.profit_and_loss.router import (
    router as profit_and_loss_router,
)
from app.modules.balance_sheet.router import (
    router as balance_sheet_router,
)
from app.modules.cash_flow.router import (
    router as cash_flow_router,
)
from app.modules.dashboard.router import (
    router as dashboard_router,
)
from fastapi.middleware.cors import CORSMiddleware                                                                  

app = FastAPI(
    title="Granite ERP Pro API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(branch_router)
app.include_router(employee_router)
app.include_router(customer_router)
app.include_router(department_router)
app.include_router(designation_router)
app.include_router(supplier_router)
app.include_router(product_category_router)
app.include_router(uom_router)
app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(stock_router)
app.include_router(stock_movement_router)
app.include_router(purchase_order_router)
app.include_router(grn_router)
app.include_router(purchase_invoice_router)
app.include_router(delivery_challan_router)
app.include_router(sales_invoice_router)
app.include_router(customer_payment_router)
app.include_router(supplier_payment_router)
app.include_router(accounts_receivable_router)
app.include_router(accounts_payable_router)
app.include_router(chart_of_accounts_router)
app.include_router(journal_entries_router)
app.include_router(general_ledger_router)
app.include_router(trial_balance_router)
app.include_router(profit_and_loss_router)
app.include_router(balance_sheet_router)
app.include_router(cash_flow_router)
app.include_router(dashboard_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {
        "message": "Granite ERP Pro API",
        "status": "running",
    }