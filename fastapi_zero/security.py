from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

SECRET_KEY = '05b3cb9e11dbe8dddfb3a65b016e6a9ce0794567e46b9f88bab42d8a5f2da43b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
