from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.core.roles import UserRole
from app.modules.auth.permissions import require_roles

from app.modules.department.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
)

from app.modules.department.service import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post("/", response_model=DepartmentResponse)
def create(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    try:
        return create_department(db, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[DepartmentResponse])
def list_all(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_departments(db)


@router.get("/{department_id}",
            response_model=DepartmentResponse)
def get_one(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    department = get_department(
        db,
        department_id,
    )

    if department is None:
        raise HTTPException(
            404,
            "Department not found",
        )

    return department


@router.put("/{department_id}",
            response_model=DepartmentResponse)
def update(
    department_id: UUID,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    department = update_department(
        db,
        department_id,
        data,
    )

    if department is None:
        raise HTTPException(
            404,
            "Department not found",
        )

    return department


@router.delete("/{department_id}")
def delete(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    department = delete_department(
        db,
        department_id,
    )

    if department is None:
        raise HTTPException(
            404,
            "Department not found",
        )

    return {
        "message": "Department deleted successfully"
    }