from datetime import datetime, timedelta
import jwt
from bcrypt import hashpw, gensalt, checkpw
from fastapi import HTTPException, status
from core.settings import settings


def get_hashed_password(password):
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    return hashed_password.decode("utf-8")


def verify_password(password, hashed_db_password):
    return checkpw(password.encode('utf-8'), hashed_db_password.encode("utf-8"))


def create_access_token(user_id: int):
    payload = {
        "expire": str(datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
        "issued": str(datetime.utcnow()),
        "subject": str(user_id),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return f"Bearer {token}"


def decode_access_token(token: str):
    try:
        if token is not None:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized."
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature expired. Please log in again."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please log in again."
        )
