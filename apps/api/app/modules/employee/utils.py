from sqlalchemy.orm import Session

from app.models.employee import Employee


def generate_employee_code(db: Session) -> str:
    count = db.query(Employee).count() + 1
    return f"EMP{count:04d}"