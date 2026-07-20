from sqlalchemy.orm import Session

from app.models.company import Company
from app.modules.company.schemas import CompanyCreate, CompanyUpdate


def create_company(db: Session, company: CompanyCreate):
    existing = db.query(Company).filter(
        Company.code == company.code
    ).first()

    if existing:
        raise ValueError("Company code already exists")

    new_company = Company(**company.model_dump())

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


def get_companies(db: Session):
    return db.query(Company).filter(
        Company.is_deleted == False
    ).all()


def get_company(db: Session, company_id):
    return db.query(Company).filter(
        Company.id == company_id,
        Company.is_deleted == False,
    ).first()


def update_company(db: Session, company_id, data: CompanyUpdate):
    company = get_company(db, company_id)

    if not company:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


def delete_company(db: Session, company_id):
    company = get_company(db, company_id)

    if not company:
        return None

    company.is_deleted = True

    db.commit()

    return company