from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.modules.warehouse.schemas import (
    WarehouseCreate,
    WarehouseUpdate,
)


def create_warehouse(
    db: Session,
    warehouse: WarehouseCreate,
):
    existing = (
        db.query(Warehouse)
        .filter(
            Warehouse.warehouse_code == warehouse.warehouse_code
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Warehouse code already exists"
        )

    new_warehouse = Warehouse(
        **warehouse.model_dump()
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)

    return new_warehouse


def get_warehouses(db: Session):
    return db.query(Warehouse).all()


def get_warehouse(
    db: Session,
    warehouse_id,
):
    return (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id)
        .first()
    )


def update_warehouse(
    db: Session,
    warehouse_id,
    warehouse: WarehouseUpdate,
):
    db_warehouse = get_warehouse(
        db,
        warehouse_id,
    )

    if not db_warehouse:
        return None

    for key, value in warehouse.model_dump().items():
        setattr(db_warehouse, key, value)

    db.commit()
    db.refresh(db_warehouse)

    return db_warehouse


def delete_warehouse(
    db: Session,
    warehouse_id,
):
    db_warehouse = get_warehouse(
        db,
        warehouse_id,
    )

    if not db_warehouse:
        return False

    db.delete(db_warehouse)
    db.commit()

    return True