# ORM models for columns definition of the DB tables
# using Base class from database.py
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .database import Base


# ORM model for Post
class Post(Base):
    __tablename__ = "posts"

    # this is serial type, if autoincrement is set to false then it won't be serial
    p_id = Column(Integer, primary_key=True, nullable=False)
    p_title = Column(String, nullable=False)
    p_content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # creating a foreign key named owner_id to reference u_id in 'users' table, here we are referring the DB not ORM hence we refer to table not class.
    owner_id = Column(
        Integer, ForeignKey("users.u_id", ondelete="CASCADE"), nullable=False
    )
    # get the user entry specific to owner_id. This is an ORM operation so we refer to User class. We get an ORM model of that user row.
    owner = relationship("User")


# ORM model for User
class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, nullable=False)
    u_email = Column(String, nullable=False, unique=True)
    u_password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# ORM model for Vote
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(
        Integer, ForeignKey("posts.p_id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.u_id", ondelete="CASCADE"), primary_key=True
    )
