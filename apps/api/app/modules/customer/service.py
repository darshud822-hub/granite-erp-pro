from uuid import UUID

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.company import Company
from app.models.branch import Branch

from app.modules.customer.schemas import (
    CustomerCreate,
    CustomerUpdate,
)

from app.modules.customer.utils import (
    generate_customer_code,
)


def create_customer(db: Session, customer: CustomerCreate):

    company = db.query(Company).filter(
        Company.id == customer.company_id
    ).first()

    if not company:
        raise ValueError("Company not found")

    branch = db.query(Branch).filter(
        Branch.id == customer.branch_id
    ).first()

    if not branch:
        raise ValueError("Branch not found")

    if branch.company_id != customer.company_id:
        raise ValueError(
            "Branch does not belong to selected company"
        )

    if db.query(Customer).filter(
        Customer.email == customer.email
    ).first():
        raise ValueError("Email already exists")

    if db.query(Customer).filter(
        Customer.phone == customer.phone
    ).first():
        raise ValueError("Phone already exists")

    new_customer = Customer(
        customer_code=generate_customer_code(db),
        **customer.model_dump()
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_customers(db: Session):
    return db.query(Customer).filter(
        Customer.is_deleted == False
    ).all()


def get_customer(db: Session, customer_id: UUID):
    return db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.is_deleted == False,
    ).first()


def update_customer(
    db: Session,
    customer_id: UUID,
    data: CustomerUpdate,
):
    customer = get_customer(db, customer_id)

    if customer is None:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(
    db: Session,
    customer_id: UUID,
):
    customer = get_customer(db, customer_id)

    if customer is None:
        return None

    customer.is_deleted = True

    db.commit()

    return customer