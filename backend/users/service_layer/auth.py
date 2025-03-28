from datetime import datetime, timezone, timedelta

from authlib.jose import jwt
from passlib.context import CryptContext
from backend.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.get_auth_data

    encode_jwt = jwt.encode(**{
        'header': {'alg': auth_data['algorithm']},
        'payload': to_encode,
        'key': auth_data['secret_key'],
    })

    return encode_jwt






