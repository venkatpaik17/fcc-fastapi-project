# schemas/pydantic models for request and response structure
from datetime import datetime

from pydantic import BaseModel, EmailStr


# Models for Posts
class PostBase(BaseModel):  # base model for posts entity
    p_title: str
    p_content: str
    published: bool = True


class PostCreate(PostBase):  # model for create/update posts request
    pass


class Post(PostBase):  # model for posts response
    p_id: int
    created_at: datetime

    class Config:  # pydantic model will read ORM model data too since pydantic reads only dict
        orm_mode = True


# Models for Users
class UserBase(BaseModel):
    u_email: EmailStr  # email validator


class UserCreate(UserBase):
    u_password: str


class User(UserBase):
    u_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(UserCreate):
    pass
