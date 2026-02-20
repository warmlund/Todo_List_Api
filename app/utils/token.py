import jwt
from datetime import datetime, timedelta, timezone
from models.user import User
from app.db import SessionDep

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30


def create_user_token(user: User):
    payload = {
        "sub": user.id,
        "name": user.name,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRES_MINUTES)
    }   
    encode_token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    return encode_token