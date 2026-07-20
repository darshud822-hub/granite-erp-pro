from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.company import Company
from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

from app.modules.company.schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)

from app.modules.company.service import (
    create_company,
    get_companies,
    get_company,
    update_company,
    delete_company,
)

router = APIRouter(
    prefix="/companies",
    tags=["Company"],
)


@router.post(
    "/",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    try:
        return create_company(db, company)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[CompanyResponse],
)
def get_all(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return get_companies(db)


@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_one(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    company = get_company(db, company_id)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company


@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
)
def update(
    company_id: UUID,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    company = update_company(db, company_id, data)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company


@router.delete("/{company_id}")
def delete(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    company = delete_company(db, company_id)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return {
        "message": "Company deleted successfully"
    }