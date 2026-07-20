from pydantic import BaseModel, EmailStr
from app.core.roles import UserRole


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.SALES


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole