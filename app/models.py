# ORM models for columns definition of the DB tables
# using Base class from database.py
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    p_id = Column(
        Integer, primary_key=True, nullable=False
    )  # this is serial type, if autoincrement is set to false then it won't be serial
    p_title = Column(String, nullable=False)
    p_content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, nullable=False)
    u_email = Column(String, nullable=False, unique=True)
    u_password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
