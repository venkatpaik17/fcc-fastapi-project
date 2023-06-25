# module for defining utility functions
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash the plain text password
def get_hash(password: str):
    return pwd_context.hash(password)


# verify attempt password with DB stored hashed password
def verify_password(provided_password: str, hashed_password: str):
    return pwd_context.verify(provided_password, hashed_password)
