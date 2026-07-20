from app.models.customer import Customer
from app.models.employee import Employee
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Branch(BaseModel):
    __tablename__ = "branches"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(150))
    code: Mapped[str] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(500))

    company = relationship(
        "Company",
        back_populates="branches",
    )
    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    back_populates="branch",
    cascade="all, delete-orphan",
   )
    customers: Mapped[list["Customer"]] = relationship(
    "Customer",
    back_populates="branch",
    cascade="all, delete-orphan",
   )
    suppliers = relationship(
    "Supplier",
    back_populates="branch",
    cascade="all, delete-orphan",
)