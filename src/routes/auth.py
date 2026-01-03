from fastapi import APIRouter , HTTPException , Depends ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from dotenv import load_dotenv 
from datetime import timedelta , timezone
import os 

from ..db.database import get_db , engine
from ..db import schemas , models
from ..util.jwt import create_access_token , create_refresh_token
from ..util.password_hashing import hash_password , verify_hash_password

router = APIRouter(
    prefix="/user/regirster",
    tags=["AUTHENTICATION"]
)


@router.post("/regirster",response_model=schemas.TokenResponse)
def regirster_user(user:schemas.userCreate, db:Session = Depends(get_db)):
    exists_username = db.query(models.User).filter(models.User.username == user.username).first()
    exists_email = db.query(models.User).filter(models.User.email == user.email).first()

    if exists_username or exists_email :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="USER ALREADY EXISTS"
        )
    
    hashed_password = hash_password(user.password)

    print(f"DEBUG - user object: {user}")
    print(f"DEBUG - user.username: {user.username}")
    print(f"DEBUG - user.email: {user.email}")
    print(f"DEBUG - type: {type(user)}")

    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )
    print(f"DEBUG - Created user object: {new_user}")
    print(f"DEBUG - Username: {new_user.username}")
    
    db.add(new_user)
    print("DEBUG - Added to session")
    
    db.commit()
    print("DEBUG - Committed to database")
    
    db.refresh(new_user)
    print(f"DEBUG - User ID after refresh: {new_user.id}")

    access_token = create_access_token({"sub":str(new_user.id)})
    refresh_token= create_access_token({"sub":str(new_user.id)})

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }