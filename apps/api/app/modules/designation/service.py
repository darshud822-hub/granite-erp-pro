from sqlalchemy.orm import Session

from app.models.designation import Designation
from app.modules.designation.schemas import (
    DesignationCreate,
    DesignationUpdate,
)


def create_designation(
    db: Session,
    designation: DesignationCreate,
):
    existing = (
        db.query(Designation)
        .filter(
            (Designation.name == designation.name)
            | (Designation.code == designation.code)
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Designation name or code already exists"
        )

    new_designation = Designation(
        name=designation.name,
        code=designation.code,
        description=designation.description,
    )

    db.add(new_designation)
    db.commit()
    db.refresh(new_designation)

    return new_designation


def get_designations(db: Session):
    return db.query(Designation).all()


def get_designation(
    db: Session,
    designation_id,
):
    return (
        db.query(Designation)
        .filter(Designation.id == designation_id)
        .first()
    )


def update_designation(
    db: Session,
    designation_id,
    designation: DesignationUpdate,
):
    db_designation = get_designation(
        db,
        designation_id,
    )

    if not db_designation:
        return None

    db_designation.name = designation.name
    db_designation.code = designation.code
    db_designation.description = designation.description

    db.commit()
    db.refresh(db_designation)

    return db_designation


def delete_designation(
    db: Session,
    designation_id,
):
    designation = get_designation(
        db,
        designation_id,
    )

    if not designation:
        return False

    db.delete(designation)
    db.commit()

    return True