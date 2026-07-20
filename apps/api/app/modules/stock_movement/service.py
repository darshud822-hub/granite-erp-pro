from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.models.stock_movement import StockMovement
from app.modules.stock_movement.schemas import (
    StockMovementCreate,
    StockMovementUpdate,
)


def create_stock_movement(
    db: Session,
    movement: StockMovementCreate,
):
    existing = (
        db.query(StockMovement)
        .filter(
            StockMovement.movement_no == movement.movement_no
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Movement number already exists."
        )

    stock = (
        db.query(Stock)
        .filter(
            Stock.product_id == movement.product_id,
            Stock.warehouse_id == movement.warehouse_id,
        )
        .first()
    )

    if not stock:
        raise ValueError(
            "Stock record not found."
        )

    qty = Decimal(movement.quantity)

    if movement.movement_type.lower() in [
        "purchase",
        "receipt",
        "adjustment_in",
    ]:
        stock.quantity += qty

    elif movement.movement_type.lower() in [
        "sale",
        "damage",
        "adjustment_out",
    ]:
        if stock.quantity < qty:
            raise ValueError(
                "Insufficient stock."
            )

        stock.quantity -= qty

    stock.available_quantity = (
        stock.quantity - stock.reserved_quantity
    )

    movement_row = StockMovement(
        **movement.model_dump()
    )

    db.add(movement_row)

    db.commit()

    db.refresh(movement_row)

    return movement_row


def get_movements(db: Session):
    return db.query(StockMovement).all()


def get_movement(db: Session, movement_id):
    return (
        db.query(StockMovement)
        .filter(
            StockMovement.id == movement_id
        )
        .first()
    )


def delete_movement(
    db: Session,
    movement_id,
):
    movement = get_movement(
        db,
        movement_id,
    )

    if not movement:
        return False

    db.delete(movement)
    db.commit()

    return True