from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

# SQLALCHEMY_DATABASE_URL = "postgresql://vpk:vpk123#@localhost/fcc-fastapi"  # db url to connect, bad practice of hardcoding

# use env variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_hostname}:{config.settings.database_port}/{config.settings.database_name}"

# engine is responsible for sqlalchemy to connect to a DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# this is a session class, each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this returns a base class which we will inherit to create each database models/ORM models
Base = declarative_base()


# create a session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
