from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime

    #converts the (sqlalchemy model data) to a pydantic model
    class config:
        orm_mode = True
        
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    #converts the post(sqlalchemy model data) to a pydantic model  which is a dictionary
    class Config:
        orm_mode = True

class PostLikesResponse(BaseModel):
    Post: PostResponse
    likes: int

    #converts the post(sqlalchemy model data) to a pydantic model  which is a dictionary
    class config:
        orm_mode = True

class CreateUsers(BaseModel):
    email: EmailStr 
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

    #converts the (sqlalchemy model data) to a pydantic model
    class config:
        orm_mode = True

class TokenData(BaseModel):
    id: int


class AllUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    #converts the (sqlalchemy model data) to a pydantic model
    class config:
        orm_mode = True

class Likes(BaseModel):
    post_id: int
    liked: bool

class LikesResponse(BaseModel):
    post_id: int
    liked: bool

    #converts the (sqlalchemy model data) to a pydantic model
    class config:
        orm_mode = True