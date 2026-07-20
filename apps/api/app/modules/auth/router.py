from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.modules.auth.schemas import UserRegister, Token
from app.modules.auth.service import register_user, login_user
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.permissions import require_roles
from app.core.roles import UserRole

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
    }


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user)

        return {
            "message": "User registered successfully",
            "id": str(new_user.id),
            "username": new_user.username,
            "role": new_user.role,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = login_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return token


@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    return {
        "message": "Welcome Admin",
        "user": current_user.username,
        "role": current_user.role,
    }


@router.get("/manager")
def manager_dashboard(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
):
    return {
        "message": "Manager Dashboard",
        "user": current_user.username,
    }


@router.get("/sales")
def sales_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.SALES)
    ),
):
    return {
        "message": "Sales Dashboard",
        "user": current_user.username,
    }