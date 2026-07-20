from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.modules.stock.schemas import (
    StockCreate,
    StockUpdate,
)


def create_stock(
    db: Session,
    stock: StockCreate,
):
    existing = (
        db.query(Stock)
        .filter(
            Stock.product_id == stock.product_id,
            Stock.warehouse_id == stock.warehouse_id,
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Stock already exists for this product in this warehouse."
        )

    new_stock = Stock(**stock.model_dump())

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock


def get_stocks(db: Session):
    return db.query(Stock).all()


def get_stock(
    db: Session,
    stock_id,
):
    return (
        db.query(Stock)
        .filter(Stock.id == stock_id)
        .first()
    )


def update_stock(
    db: Session,
    stock_id,
    stock: StockUpdate,
):
    db_stock = get_stock(db, stock_id)

    if not db_stock:
        return None

    for key, value in stock.model_dump().items():
        setattr(db_stock, key, value)

    db.commit()
    db.refresh(db_stock)

    return db_stock


def delete_stock(
    db: Session,
    stock_id,
):
    db_stock = get_stock(db, stock_id)

    if not db_stock:
        return False

    db.delete(db_stock)
    db.commit()

    return True