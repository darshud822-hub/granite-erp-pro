from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.employee.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)
from app.modules.employee.service import (
    create_employee,
    get_employees,
    get_employee,
    update_employee,
    delete_employee,
)

from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post(
    "/",
    response_model=EmployeeResponse,
)
def create(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_employee(db, employee)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[EmployeeResponse],
)
def list_all(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER)),
):
    return get_employees(db)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_one(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER)),
):
    employee = get_employee(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def update(
    employee_id: UUID,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    employee = update_employee(
        db,
        employee_id,
        data,
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@router.delete("/{employee_id}")
def delete(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    employee = delete_employee(
        db,
        employee_id,
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "message": "Employee deleted successfully"
    }