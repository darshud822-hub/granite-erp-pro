from uuid import UUID

from sqlalchemy.orm import Session

from app.models.department import Department
from app.modules.department.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
)


def create_department(db: Session, data: DepartmentCreate):
    existing = db.query(Department).filter(
        (Department.name == data.name) |
        (Department.code == data.code)
    ).first()

    if existing:
        raise ValueError(
            "Department name or code already exists"
        )

    department = Department(**data.model_dump())

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_departments(db: Session):
    return db.query(Department).filter(
        Department.is_deleted == False
    ).all()


def get_department(db: Session, department_id: UUID):
    return db.query(Department).filter(
        Department.id == department_id,
        Department.is_deleted == False,
    ).first()


def update_department(
    db: Session,
    department_id: UUID,
    data: DepartmentUpdate,
):
    department = get_department(db, department_id)

    if not department:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


def delete_department(
    db: Session,
    department_id: UUID,
):
    department = get_department(db, department_id)

    if not department:
        return None

    department.is_deleted = True

    db.commit()

    return department