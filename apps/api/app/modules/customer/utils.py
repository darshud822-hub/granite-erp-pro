from sqlalchemy.orm import Session

from app.models.customer import Customer


def generate_customer_code(db: Session) -> str:
    count = db.query(Customer).count() + 1
    return f"CUS{count:04d}"