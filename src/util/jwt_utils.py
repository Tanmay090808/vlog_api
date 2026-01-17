from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from typing import Optional, Dict, Any

load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} is missing in environment")
    return value


SECRET_KEY = get_env("SECRET_KEY")
ALGORITHM = get_env("ALGORITHM")

ACCESS_TOKEN_EXPIRES_IN_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRES_IN_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def _create_token(data: Dict[str, Any], expires: datetime, token_type: str) -> str:
    to_encode = data.copy()
    to_encode.update({
        "exp": int(expires.timestamp()),
        "type": token_type
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    expires = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    )
    return _create_token(data, expires, "access")


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    expires = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRES_IN_DAYS)
    )
    return _create_token(data, expires, "refresh")


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    payload = decode_access_token(token)

    if payload.get("type") != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    return payload


def create_email_verification_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "user_id": user_id,
        "purpose": "email_verification",
        "exp": int(expires.timestamp())
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
