from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    #converts the post(sqlalchemy model data) to a pydantic model  which is a dictionary
    class config:
        orm_mode = True

class CreateUsers(BaseModel):
    email: EmailStr 
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime

    #converts the (sqlalchemy model data) to a pydantic model
    class config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str