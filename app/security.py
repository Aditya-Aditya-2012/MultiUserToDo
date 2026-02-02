#utility for creating and hashing passwords
from passlib.hash import bcrypt
from datetime import datetime, timezone, timedelta
from jose import jwt
from typing import Optional

SECRET_KEY = "my-secret-key"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=20

def get_hash(password: str):
    return bcrypt.hash(password)

def verify_password(password, hash):
    return bcrypt.verify(password, hash)

def create_access_token(data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=expire_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

