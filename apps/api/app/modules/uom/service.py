from sqlalchemy.orm import Session

from app.models.uom import UOM
from app.modules.uom.schemas import (
    UOMCreate,
    UOMUpdate,
)


def create_uom(
    db: Session,
    uom: UOMCreate,
):
    existing = (
        db.query(UOM)
        .filter(
            (UOM.name == uom.name)
            | (UOM.code == uom.code)
        )
        .first()
    )

    if existing:
        raise ValueError(
            "UOM name or code already exists"
        )

    new_uom = UOM(
        name=uom.name,
        code=uom.code,
        description=uom.description,
    )

    db.add(new_uom)
    db.commit()
    db.refresh(new_uom)

    return new_uom


def get_uoms(db: Session):
    return db.query(UOM).all()


def get_uom(
    db: Session,
    uom_id,
):
    return (
        db.query(UOM)
        .filter(UOM.id == uom_id)
        .first()
    )


def update_uom(
    db: Session,
    uom_id,
    uom: UOMUpdate,
):
    db_uom = get_uom(
        db,
        uom_id,
    )

    if not db_uom:
        return None

    db_uom.name = uom.name
    db_uom.code = uom.code
    db_uom.description = uom.description

    db.commit()
    db.refresh(db_uom)

    return db_uom


def delete_uom(
    db: Session,
    uom_id,
):
    db_uom = get_uom(
        db,
        uom_id,
    )

    if not db_uom:
        return False

    db.delete(db_uom)
    db.commit()

    return True