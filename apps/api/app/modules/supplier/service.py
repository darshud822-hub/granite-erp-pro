from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.modules.supplier.schemas import (
    SupplierCreate,
    SupplierUpdate,
)


def create_supplier(db: Session, supplier: SupplierCreate):
    existing = (
        db.query(Supplier)
        .filter(
            (Supplier.supplier_code == supplier.supplier_code)
            | (Supplier.email == supplier.email)
            | (Supplier.phone == supplier.phone)
        )
        .first()
    )

    if existing:
        raise ValueError(
            "Supplier code, email or phone already exists"
        )

    new_supplier = Supplier(
        supplier_code=supplier.supplier_code,
        company_name=supplier.company_name,
        contact_person=supplier.contact_person,
        email=supplier.email,
        phone=supplier.phone,
        gst_number=supplier.gst_number,
        address=supplier.address,
        city=supplier.city,
        state=supplier.state,
        country=supplier.country,
        pincode=supplier.pincode,
        credit_limit=supplier.credit_limit,
        outstanding_balance=supplier.outstanding_balance,
        notes=supplier.notes,
        company_id=supplier.company_id,
        branch_id=supplier.branch_id,
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier


def get_suppliers(db: Session):
    return db.query(Supplier).all()


def get_supplier(db: Session, supplier_id):
    return (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )


def update_supplier(
    db: Session,
    supplier_id,
    supplier: SupplierUpdate,
):
    db_supplier = get_supplier(db, supplier_id)

    if not db_supplier:
        return None

    db_supplier.supplier_code = supplier.supplier_code
    db_supplier.company_name = supplier.company_name
    db_supplier.contact_person = supplier.contact_person
    db_supplier.email = supplier.email
    db_supplier.phone = supplier.phone
    db_supplier.gst_number = supplier.gst_number
    db_supplier.address = supplier.address
    db_supplier.city = supplier.city
    db_supplier.state = supplier.state
    db_supplier.country = supplier.country
    db_supplier.pincode = supplier.pincode
    db_supplier.credit_limit = supplier.credit_limit
    db_supplier.outstanding_balance = supplier.outstanding_balance
    db_supplier.notes = supplier.notes
    db_supplier.company_id = supplier.company_id
    db_supplier.branch_id = supplier.branch_id

    db.commit()
    db.refresh(db_supplier)

    return db_supplier


def delete_supplier(db: Session, supplier_id):
    supplier = get_supplier(db, supplier_id)

    if not supplier:
        return False

    db.delete(supplier)
    db.commit()

    return True