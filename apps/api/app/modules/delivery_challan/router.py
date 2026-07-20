from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.delivery_challan.schemas import (
    DeliveryChallanCreate,
    DeliveryChallanResponse,
)

from app.modules.delivery_challan.service import (
    create_delivery_challan,
    get_delivery_challans,
    get_delivery_challan,
    delete_delivery_challan,
)

router = APIRouter(
    prefix="/delivery-challans",
    tags=["Delivery Challans"],
)


@router.post("/", response_model=DeliveryChallanResponse)
def create(
    challan: DeliveryChallanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.PRODUCTION,
)
    ),
):
    try:
        return create_delivery_challan(db, challan)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/", response_model=list[DeliveryChallanResponse])
def get_all(
    db: Session = Depends(get_db),
):
    return get_delivery_challans(db)


@router.get("/{challan_id}", response_model=DeliveryChallanResponse)
def get_one(
    challan_id: UUID,
    db: Session = Depends(get_db),
):
    challan = get_delivery_challan(db, challan_id)

    if not challan:
        raise HTTPException(
            status_code=404,
            detail="Delivery Challan not found",
        )

    return challan


@router.delete("/{challan_id}")
def delete(
    challan_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    deleted = delete_delivery_challan(db, challan_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Delivery Challan not found",
        )

    return {
        "message": "Delivery Challan deleted successfully"
    }