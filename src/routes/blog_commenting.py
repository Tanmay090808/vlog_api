from fastapi import APIRouter , HTTPException , Depends ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from dotenv import load_dotenv 
from datetime import timedelta , timezone , datetime
from typing import List

from ..db.database import get_db , engine
from ..db import schemas , models
from ..util.jwt import create_access_token , create_refresh_token
from ..util.password_hashing import hash_password , verify_hash_password
from ..util.oauth2  import security
from ..util.dependencies import get_current_user

router = APIRouter(
    prefix="/comment-to-blog",
    tags=["COMMENT_SECTION"]
)

@router.post("/blogs/{blog_id}/comments", response_model=schemas.CommentResponse)
def add_comment(
    blog_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(404, "Blog not found")

    new_comment = models.Comment(
        content=comment.content,
        blog_id=blog_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
