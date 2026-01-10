from fastapi import APIRouter , HTTPException , Depends ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from dotenv import load_dotenv 
from datetime import timedelta , timezone , datetime
import os 

from ..db.database import get_db , engine
from ..db import schemas , models
from ..util.jwt import create_access_token , create_refresh_token , create_email_verification_token
from ..util.password_hashing import hash_password , verify_hash_password
from ..util.oauth2  import security
from ..util.dependencies import get_current_user
from ..util.email_verification import send_verification_email

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


    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )
    
    db.add(new_user)    
    db.commit()    
    db.refresh(new_user)

    
    token = create_email_verification_token(new_user.id)

    # 4️⃣ Send verification email
    send_verification_email(user.email, token)

    # 5️⃣ Return response (NO TOKEN)
    return {
        "message": "Registration successful. Please verify your email."
    }

@router.post("/user/login",response_model=schemas.TokenResponse)
def login_user(form_data:OAuth2PasswordRequestForm =Depends(),db:Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    is_valid = verify_hash_password(form_data.password , str(user.hashed_password))

    if not is_valid :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    payload = {
        "user_id":user.id,
        "username":user.username
    }

    access_token = create_access_token(payload)
    refresh_token_string = create_refresh_token({"sub": user.id})
    expires_at = datetime.utcnow() + timedelta(days=7)
    expires_at = datetime.utcnow() + timedelta(days=7)

    new_refresh_token = models.RefreshToken(
        user_id = user.id,
        token = refresh_token_string,
        expires_at = expires_at,
        is_revoked = False,
        device_logged_in ="web"
    )

    db.add(new_refresh_token)
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_string,
        "token_type": "bearer"
    }
@router.get("/user/get-current")
def get_logged_in_user(
    current_user: models.User = Depends(get_current_user),  # Accept User object
):
    # current_user is already the User object, just return it
    return current_user


@router.put("/user/change-password/{email}")
def change_password(
    email: str,
    password_in: schemas.change_password_in,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(password_in.new_password)

    db.commit()        # works
    db.refresh(user)   # works

    return {"message": "Password updated"}
