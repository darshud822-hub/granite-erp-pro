from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.stock.schemas import (
    StockCreate,
    StockUpdate,
    StockResponse,
)

from app.modules.stock.service import (
    create_stock,
    get_stocks,
    get_stock,
    update_stock,
    delete_stock,
)

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
)


@router.post("/", response_model=StockResponse)
def create(
    stock: StockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER)),
):
    try:
        return create_stock(db, stock)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StockResponse])
def get_all(db: Session = Depends(get_db)):
    return get_stocks(db)


@router.get("/{stock_id}", response_model=StockResponse)
def get_one(stock_id: UUID, db: Session = Depends(get_db)):
    stock = get_stock(db, stock_id)

    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    return stock


@router.put("/{stock_id}", response_model=StockResponse)
def update(
    stock_id: UUID,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    updated = update_stock(db, stock_id, stock)

    if not updated:
        raise HTTPException(status_code=404, detail="Stock not found")

    return updated


@router.delete("/{stock_id}")
def delete(
    stock_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    deleted = delete_stock(db, stock_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Stock not found")

    return {
        "message": "Stock deleted successfully"
    }