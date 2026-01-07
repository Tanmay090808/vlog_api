from jose import jwt , JWTError
from dotenv import load_dotenv 
import os 
from datetime import timedelta  , datetime , timezone
from fastapi import HTTPException ,status
from typing import Optional , Dict , Optional,Any

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_IN_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","15"))
REFRESH_TOKEN_EXPIRES_IN_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS","7"))

def create_access_token(Data:Dict[str,Any],expires_delta:Optional[timedelta]=None)->str:
    to_encode =Data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRES_IN_MINUTES)

    to_encode.update({
        "exp":int(expires.timestamp()),
        "type":"access"
    })

    encoded_jwt = jwt.encode(to_encode ,SECRET_KEY,algorithm=ALGORITHM) #type:ignore

    return encoded_jwt

def create_refresh_token(Data:Dict[str,Any],expires_delta:Optional[timedelta]=None)->str:
    to_encode = Data.copy()

    if expires_delta :
        expires = datetime.now(timezone.utc) + expires_delta
    else :
        expires = datetime.now(timezone.utc) +timedelta(REFRESH_TOKEN_EXPIRES_IN_DAYS )

    to_encode.update({
        "exp":int(expires.timestamp()),
        "type":"access"
    })

    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM) #type:ignore

    return encoded_jwt


def verify_token(token: str, token_type: str = "access") ->Dict:
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM]) #type:ignore
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_token_expiry(token_type: str = "access") -> datetime:
    if token_type == "access":
        return datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN_MINUTES)
    else:  # refresh
        return datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRES_IN_DAYS)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type:ignore
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )
    
