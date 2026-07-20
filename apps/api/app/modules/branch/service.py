from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.models.company import Company
from app.modules.branch.schemas import BranchCreate, BranchUpdate


def create_branch(db: Session, branch: BranchCreate):

    company = db.query(Company).filter(
        Company.id == branch.company_id
    ).first()

    if not company:
        raise ValueError("Company not found")

    existing = db.query(Branch).filter(
        Branch.code == branch.code
    ).first()

    if existing:
        raise ValueError("Branch code already exists")

    new_branch = Branch(**branch.model_dump())

    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return new_branch


def get_branches(db: Session):
    return db.query(Branch).filter(
        Branch.is_deleted == False
    ).all()


def get_branch(db: Session, branch_id):
    return db.query(Branch).filter(
        Branch.id == branch_id,
        Branch.is_deleted == False,
    ).first()


def update_branch(db: Session, branch_id, data: BranchUpdate):
    branch = get_branch(db, branch_id)

    if not branch:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(branch, key, value)

    db.commit()
    db.refresh(branch)

    return branch


def delete_branch(db: Session, branch_id):
    branch = get_branch(db, branch_id)

    if not branch:
        return None

    branch.is_deleted = True

    db.commit()

    return branch