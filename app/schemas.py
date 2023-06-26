# schemas/pydantic models for request and response structure
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Models for Users
class UserBase(BaseModel):  # base model for users entity
    u_email: EmailStr  # email validator


class UserCreate(UserBase):  # model for create/update user request
    u_password: str


class User(UserBase):  # model for user response
    u_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(UserCreate):  # model for user login request
    pass


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
    owner_id: int  # this is added here instead of PostBase because we don't want user to explicitly add owner_id, request logic should handle it.
    owner: User  # the user ORM model we get from relationship ORM operation is parsed as pydantic/schema model

    class Config:  # setting orm_mode as True. pydantic model will read ORM model data too since pydantic reads only dict
        orm_mode = True


# model for generated token
class Token(BaseModel):
    access_token: str
    token_type: str


# model for payload data extracted from token during token verification
class TokenData(BaseModel):
    u_id: Optional[int] = None
