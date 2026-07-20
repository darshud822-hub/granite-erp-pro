from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.purchase_order.schemas import (
    PurchaseOrderCreate,
    PurchaseOrderResponse,
)

from app.modules.purchase_order.service import (
    create_purchase_order,
    get_purchase_orders,
    get_purchase_order,
    delete_purchase_order,
)

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)


@router.post("/", response_model=PurchaseOrderResponse)
def create(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_purchase_order(
            db,
            purchase_order,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[PurchaseOrderResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_purchase_orders(db)


@router.get("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def get_one(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
):
    purchase_order = get_purchase_order(
        db,
        purchase_order_id,
    )

    if not purchase_order:
        raise HTTPException(
            status_code=404,
            detail="Purchase Order not found",
        )

    return purchase_order


@router.delete("/{purchase_order_id}")
def delete(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_purchase_order(
        db,
        purchase_order_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Purchase Order not found",
        )

    return {
        "message": "Purchase Order deleted successfully"
    }