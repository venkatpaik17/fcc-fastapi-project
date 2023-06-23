# ORM models for columns definition of the DB tables
# using Base class from database.py
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, true

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    p_id = Column(Integer, primary_key=True, nullable=False)
    p_title = Column(String, nullable=False)
    p_content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
