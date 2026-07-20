from datetime import datetime, timedelta, UTC

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    print("verify_password() called")
    print("Password:", repr(password))
    print("Hash:", hashed_password)

    try:
        result = pwd_context.verify(password, hashed_password)
        print("Result:", result)
        return result
    except Exception as e:
        print("ERROR:", type(e).__name__)
        print(e)
        raise

def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None