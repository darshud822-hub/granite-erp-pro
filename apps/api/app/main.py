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

@app.get("/")
def root():
    return {
        "message": "Granite ERP Pro API",
        "status": "running",
    }