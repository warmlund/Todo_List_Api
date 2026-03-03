from typing import Annotated
from pydantic import EmailStr, ValidationError
from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends

from app.db import get_session
from app.models.user import User, UserCreate, UserLogin
from app.utils.password import hash_password, verify_password
from app.utils.token import decode_user_token
from app.utils.security import oauth2_scheme

def get_user_by_email (email: EmailStr, session: Session):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user_in_db(user: UserCreate, session:Session):
    hashed_password = hash_password(user.password)
    new_user =  User(name = user.name, email = user.email, password = hashed_password )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    
    except Exception as e:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Error creating user: {e}"
        )

def verify_login(user: UserLogin, session: Session):
    existing_user = get_user_by_email(user.email, session)
    if existing_user and verify_password(user.password, existing_user.password):
            return existing_user

    return None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]) -> User:
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_exception = HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "User not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_user_token(token)

        if user_id is None:
            raise credentials_exception
        
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

    except (ValidationError, Exception):
        raise credentials_exception

    if user is None:
        raise user_exception

    return user

