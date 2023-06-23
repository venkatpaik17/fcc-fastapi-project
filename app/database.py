from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://vpk:vpk123#@localhost/fcc-fastapi"  # db url to connect, bad practice of hardcoding

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
