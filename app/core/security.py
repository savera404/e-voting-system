from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt is the industry-standard password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#pswd is saved as a hash 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#This creates the JWT token after a successful login. Step by step:
# Takes the data you want to store in the token (e.g. {"sub": voter_id})
# Calculates the expiry time (current time + 24 hours)
# Adds "exp" (expiry) into the token payload
# Signs and encodes everything using the SECRET_KEY → produces the token string

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#his is used in `dependencies.py` to verify incoming tokens. It:
# - Uses the `SECRET_KEY` to verify the signature
# - Automatically checks if the token has expired
# - If anything is wrong → raises a `JWTError` which `dependencies.py` catches and returns a 401

def decode_token(token: str) -> dict:
    """Raises jose.JWTError if the token is invalid or expired."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
