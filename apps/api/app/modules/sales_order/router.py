from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.sales_order.schemas import (
    SalesOrderCreate,
    SalesOrderResponse,
)

from app.modules.sales_order.service import (
    create_sales_order,
    get_sales_orders,
    get_sales_order,
    delete_sales_order,
)

router = APIRouter(
    prefix="/sales-orders",
    tags=["Sales Orders"],
)


@router.post("/", response_model=SalesOrderResponse)
def create(
    order: SalesOrderCreate,
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
        return create_sales_order(db, order)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[SalesOrderResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_sales_orders(db)


@router.get("/{order_id}", response_model=SalesOrderResponse)
def get_one(
    order_id: UUID,
    db: Session = Depends(get_db),
):
    order = get_sales_order(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Sales Order not found",
        )

    return order


@router.delete("/{order_id}")
def delete(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_sales_order(
        db,
        order_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Sales Order not found",
        )

    return {
        "message": "Sales Order deleted successfully"
    }