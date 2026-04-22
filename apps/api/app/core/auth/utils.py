
from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY = 3600 # 1 hour in seconds

def hash_password(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str: 
    
    expire = datetime.now() + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload = {
        "user": user_data,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        return token_data
    
    except JWTError as e:
        return None