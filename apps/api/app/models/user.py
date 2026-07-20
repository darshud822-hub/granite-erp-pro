from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
from app.models.base_model import BaseModel
from app.core.roles import UserRole

class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    role: Mapped[UserRole] = mapped_column(
    Enum(UserRole, name="userrole"),
    default=UserRole.SALES,
    nullable=False,
)

    full_name: Mapped[str | None] = mapped_column(String(150))

    hashed_password: Mapped[str] = mapped_column(String(255))

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )