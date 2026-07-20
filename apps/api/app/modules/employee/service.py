from uuid import UUID
from app.models import employee
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.company import Company
from app.models.branch import Branch

from app.modules.employee.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
)
from app.modules.employee.utils import generate_employee_code


def create_employee(db: Session, employee: EmployeeCreate):

    # Check company exists
    company = db.query(Company).filter(
        Company.id == employee.company_id
    ).first()

    if not company:
        raise ValueError("Company not found")

    # Check branch exists
    branch = db.query(Branch).filter(
        Branch.id == employee.branch_id
    ).first()

    if not branch:
        raise ValueError("Branch not found")

    # Ensure branch belongs to company
    if branch.company_id != employee.company_id:
        raise ValueError(
            "Selected branch does not belong to selected company"
        )

    # Duplicate email check
    existing = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing:
        raise ValueError("Employee email already exists")

    new_employee = Employee(
        employee_code=generate_employee_code(db),
        **employee.model_dump()
    )
    new_employee.designation_id = employee.designation_id
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def get_employees(db: Session):
    return db.query(Employee).filter(
        Employee.is_deleted == False
    ).all()


def get_employee(db: Session, employee_id: UUID):
    return db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.is_deleted == False
    ).first()


def update_employee(
    db: Session,
    employee_id: UUID,
    data: EmployeeUpdate,
):
    employee = get_employee(db, employee_id)

    if not employee:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee_id: UUID):

    employee = get_employee(db, employee_id)

    if not employee:
        return None

    employee.is_deleted = True

    db.commit()

    return employee