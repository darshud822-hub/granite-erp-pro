from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.sales_invoice.schemas import (
    SalesInvoiceCreate,
    SalesInvoiceResponse,
)

from app.modules.sales_invoice.service import (
    create_sales_invoice,
    get_sales_invoices,
    get_sales_invoice,
    delete_sales_invoice,
)

router = APIRouter(
    prefix="/sales-invoices",
    tags=["Sales Invoices"],
)


@router.post("/", response_model=SalesInvoiceResponse)
def create(
    invoice: SalesInvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.SALES,
        )
    ),
):
    try:
        return create_sales_invoice(db, invoice)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[SalesInvoiceResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_sales_invoices(db)


@router.get("/{invoice_id}", response_model=SalesInvoiceResponse)
def get_one(
    invoice_id: UUID,
    db: Session = Depends(get_db),
):
    invoice = get_sales_invoice(db, invoice_id)

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Sales Invoice not found",
        )

    return invoice


@router.delete("/{invoice_id}")
def delete(
    invoice_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_sales_invoice(
        db,
        invoice_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Sales Invoice not found",
        )

    return {
        "message": "Sales Invoice deleted successfully"
    }