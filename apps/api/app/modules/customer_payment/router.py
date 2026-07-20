from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.customer_payment.schemas import (
    CustomerPaymentCreate,
    CustomerPaymentResponse,
)

from app.modules.customer_payment.service import (
    create_customer_payment,
    get_customer_payments,
    get_customer_payment,
    delete_customer_payment,
)

router = APIRouter(
    prefix="/customer-payments",
    tags=["Customer Payments"],
)


@router.post("/", response_model=CustomerPaymentResponse)
def create(
    payment: CustomerPaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.ACCOUNTANT,
        )
    ),
):
    try:
        return create_customer_payment(db, payment)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[CustomerPaymentResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_customer_payments(db)


@router.get("/{payment_id}", response_model=CustomerPaymentResponse)
def get_one(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    payment = get_customer_payment(db, payment_id)

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Customer Payment not found",
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
    deleted = delete_customer_payment(db, payment_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer Payment not found",
        )

    return {
        "message": "Customer Payment deleted successfully"
    }