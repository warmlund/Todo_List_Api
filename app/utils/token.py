"""
JWT Token utilities for authentication

Functions for creating and decoding suer access tokens
used for authentication in protected APPI routes
"""

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
    """
    Generate a JWT access token for an authenticated user.

    The token contains user identification information and
    an expiration timestamp.

    Args:
        user: The authenticated User instance.

    Returns:
        A signed JWT access token as a string.
    """
    payload = {
        "sub": str(user.id),
        "name": user.name,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes = int(ACCESS_TOKEN_EXPIRES_MINUTES))
    }   
    encode_token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encode_token

def decode_user_token(token: str):
    """
    Decode and validate a JWT access token.

    Extracts the user ID from the token payload after verifying
    the signature and expiration.

    Args:
        token: JWT access token from the Authorization header.

    Returns:
        The user ID extracted from the token.

    Raises:
        HTTPException 401: If the token is missing or invalid.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    bytes_token = token.encode('utf-8') 
    decoded_token = jwt.decode(bytes_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = decoded_token.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return int(user_id)
