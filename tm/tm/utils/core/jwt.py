from datetime import datetime, timedelta
import pytz
import jwt
import os
from dotenv import (
    load_dotenv
)

load_dotenv(dotenv_path=".flaskenv")
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow().replace(tzinfo=pytz.utc) + expires_delta
    else:
        expire = datetime.utcnow().replace(tzinfo=pytz.utc) + timedelta(hours=6)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return (encoded_jwt, expire)


def decode_access_token(token: str) -> dict:
    decoded_token = jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        verify=True,
        algorithms=ALGORITHM
    )
    return decoded_token
