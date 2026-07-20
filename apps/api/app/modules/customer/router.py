from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.customer.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

from app.modules.customer.service import (
    create_customer,
    get_customers,
    get_customer,
    update_customer,
    delete_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
)
def create(
    customer: CustomerCreate,
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
        return create_customer(db, customer)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[CustomerResponse],
)
def list_all(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.SALES,
        )
    ),
):
    return get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_one(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.SALES,
        )
    ),
):
    customer = get_customer(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update(
    customer_id: UUID,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    customer = update_customer(
        db,
        customer_id,
        data,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.delete("/{customer_id}")
def delete(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    customer = delete_customer(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {
        "message": "Customer deleted successfully"
    }