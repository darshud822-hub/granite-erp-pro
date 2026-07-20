from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.supplier_payment.schemas import (
    SupplierPaymentCreate,
    SupplierPaymentResponse,
)

from app.modules.supplier_payment.service import (
    create_supplier_payment,
    get_supplier_payments,
    get_supplier_payment,
    delete_supplier_payment,
)

router = APIRouter(
    prefix="/supplier-payments",
    tags=["Supplier Payments"],
)


@router.post("/", response_model=SupplierPaymentResponse)
def create(
    payment: SupplierPaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
            UserRole.PURCHASE,
        )
    ),
):
    try:
        return create_supplier_payment(db, payment)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[SupplierPaymentResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_supplier_payments(db)


@router.get("/{payment_id}", response_model=SupplierPaymentResponse)
def get_one(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    payment = get_supplier_payment(db, payment_id)

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Supplier Payment not found",
        )

    return payment


@router.delete("/{payment_id}")
def delete(
    payment_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_supplier_payment(
        db,
        payment_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Supplier Payment not found",
        )

    return {
        "message": "Supplier Payment deleted successfully"
    }