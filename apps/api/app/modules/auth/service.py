from sqlalchemy.orm import Session
from app.core.roles import UserRole
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.modules.auth.schemas import UserRegister


def register_user(db: Session, user: UserRegister):
    existing = (
        db.query(User)
        .filter(
            (User.username == user.username) |
            (User.email == user.email)
        )
        .first()
    )

    if existing:
        raise ValueError("Username or email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role=user.role,  # Use the role from the registration request
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, username: str, password: str):
    print("=" * 50)
    print("Username received:", username)

    user = db.query(User).filter(User.username == username).first()

    print("User object:", user)

    if not user:
        print("❌ User not found")
        return None

    print("Stored hash:", user.hashed_password)

    password_ok = verify_password(password, user.hashed_password)

    print("Password received:", password)
    print("Password match:", password_ok)

    if not password_ok:
        print("❌ Password verification failed")
        return None

    print("✅ Login successful")

    return user


def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)

    if not user:
        print("❌ authenticate_user returned None")
        return None

    print("✅ Creating JWT for:", user.username)

    token = create_access_token(str(user.id))

    print("✅ JWT created")

    return {
        "access_token": token,
        "token_type": "bearer",
    }