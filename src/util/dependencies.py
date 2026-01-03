from fastapi import HTTPException ,Depends , status
from sqlalchemy.orm import Session
from jose import jwt , JWTError
from fastapi.security import HTTPAuthorizationCredentials
import os
from typing import Optional , Any


from ..db import schemas , models
from ..util.oauth2 import security
from ..db.database import get_db
from ..util.jwt import decode_access_token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user