from sqlalchemy import Column , Integer , Text , ForeignKey , DateTime , String , Boolean 
from sqlalchemy.orm import relationship,Mapped , mapped_column
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer , primary_key=True , nullable= False)
    username :Mapped[str] = mapped_column(String ,nullable=False , index=True)
    hashed_password:Mapped[str] = mapped_column(String , nullable= False )
    email :Mapped[str]= mapped_column(String , nullable= False , unique= True )
    role:Mapped[str]= mapped_column(String , nullable= False , default="user")
    is_verified:Mapped[bool] = mapped_column(Boolean , default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime , default=datetime.utcnow)

    refresh_token = relationship("RefreshToken",back_populates="users")
    posts = relationship("Posts", back_populates="author")

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id:Mapped[int] = mapped_column(Integer , nullable=False , primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer ,ForeignKey("users.id"))
    token :Mapped[str]= mapped_column(String , nullable=False)
    device_logged_in:Mapped[str] = mapped_column(String , default="web")
    is_revoked:Mapped[bool] = mapped_column(Boolean , default= False)
    expires_at:Mapped[datetime] = mapped_column(DateTime  , nullable=False)
    created_at:Mapped[datetime]= mapped_column(DateTime,default=datetime.utcnow)

    users = relationship("User",back_populates="refresh_token")

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    author: Mapped["User"] = relationship(back_populates="posts")
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)