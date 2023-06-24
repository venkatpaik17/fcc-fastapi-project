# module for generating jwt token
from datetime import datetime, timedelta

from jose import JWTError, jwt

# 3 things are needed
# SECRET_KEY to generate signature, stored on the server side not accessible to outside
# type of Algo to encode and sign
# Token expiration time

SECRET_KEY = "0ddef07ee02f733af33516f998b217df4938d42e472a811469bcbdd34b50b73c"  # generate this using openssl rand -hex 32, gives a random 32 bytes (256 bits) string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(payload: dict):
    # make a copy of payload to avoid changing original payload
    to_encode = payload.copy()

    # get the expiration time from now
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # we are adding expire time also to the payload
    to_encode.update({"exp": expire})

    # generate token (and internally signature)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
