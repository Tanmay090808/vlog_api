from fastapi import APIRouter , HTTPException , Depends ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from dotenv import load_dotenv 
from datetime import timedelta , timezone , datetime
import os 

from ..db.database import get_db , engine
from ..db import schemas , models
from ..util.jwt import create_access_token , create_refresh_token
from ..util.password_hashing import hash_password , verify_hash_password
from ..util.oauth2  import security
from ..util.dependencies import get_current_user

router = APIRouter(
    prefix="/upload-blog",
    tags=["UPLOAD_SECTION"]
)

@router.post("/user/blog",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate , db:Session= Depends(get_db),
                current_user :models.User = Depends(get_current_user)):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        author_id=current_user.id
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog