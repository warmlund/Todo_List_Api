import jwt
import os

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", "30")

def create_user_token(user: User):
    payload = {
        "sub": str(user.id),
        "name": user.name,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes = int(ACCESS_TOKEN_EXPIRES_MINUTES))
    }   
    encode_token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encode_token

def decode_user_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    #try:
    bytes_token = token.encode('utf-8') 
    decoded_token = jwt.decode(bytes_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = decoded_token.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return int(user_id)

    """except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")"""
