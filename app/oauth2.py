# module for generating jwt token
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import config, schemas

# 3 things are needed
# SECRET_KEY to generate signature, stored on the server side not accessible to outside
# type of Algo to encode and sign
# Token expiration time

# bad practice to store here
# SECRET_KEY = "0ddef07ee02f733af33516f998b217df4938d42e472a811469bcbdd34b50b73c"  # generate this using openssl rand -hex 32, gives a random 32 bytes (256 bits) string
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# use env variables to define these
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: dict):
    # make a copy of payload to avoid changing original payload
    to_encode = payload.copy()

    # get the expiration time from now
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # we are adding expire time also to the payload
    to_encode.update({"exp": expire})

    # generate token (and internally signature)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# verify the token and return the payload data
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    token_data = schemas.TokenData(u_id=id)
    return token_data


# this function validates the header as per oauth2 spec and calls verify_access_token function to verify the token and return payload data
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
