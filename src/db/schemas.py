from pydantic import typing , BaseModel , EmailStr , validator ,Field
import re 
from datetime import datetime 


class userCreate(BaseModel):
    username:str = Field(..., min_length=6 , max_length=50)
    email:EmailStr
    password:str = Field(..., min_length=8, max_length=40)

    @validator('username')
    def valid_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$',v):
            raise ValueError('USERNAME_MUST_CONTAIN_a-z_A-Z_0-9_')
        
        if not v[0]:
            raise ValueError('USERNAME_MUST_START_WITH_ALBHABET')
        return v
        
    @validator('email')
    def email_lowercase(cls, v):
        return v.lower()


class UaserLogin(BaseModel):
    email:EmailStr
    password :str

    @validator('email')
    def email_lowercase(cls, v):
        return v.lower()

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refreshtoken:str