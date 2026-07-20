from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.purchase_invoice.schemas import (
    PurchaseInvoiceCreate,
    PurchaseInvoiceResponse,
)

from app.modules.purchase_invoice.service import (
    create_purchase_invoice,
    get_purchase_invoices,
    get_purchase_invoice,
    delete_purchase_invoice,
)

router = APIRouter(
    prefix="/purchase-invoices",
    tags=["Purchase Invoice"],
)


@router.post("/", response_model=PurchaseInvoiceResponse)
def create_invoice(
    invoice: PurchaseInvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_purchase_invoice(db, invoice)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[PurchaseInvoiceResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_purchase_invoices(db)


@router.get("/{invoice_id}", response_model=PurchaseInvoiceResponse)
def get_one(
    invoice_id: UUID,
    db: Session = Depends(get_db),
):
    invoice = get_purchase_invoice(
        db,
        invoice_id,
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Purchase Invoice not found",
        )

    return invoice


@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_purchase_invoice(
        db,
        invoice_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Purchase Invoice not found",
        )

    return {
        "message": "Purchase Invoice deleted successfully"
    }