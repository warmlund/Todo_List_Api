"""
Functions for user operations

Helper functions for:
    - Creating user
    - Get user by email
    - Verifying user login
    - Get current user form token
"""

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
    """
    Retrieve a user from the database by email address

    Args:
        email: Email address used to identify the user
        session: Active database session

    Returns:
        The first matching User instance if found, otherwise None
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user_in_db(user: UserCreate, session:Session):
    """
    Create and store a new user in the database

    The user's password is hashed before storing

    Args:
        user: UserCreate object containing user registration data.
        session: Active database session

    Returns:
       new_user: New User instance

    Raises:
        HTTPException 400: If the user cannot be saved to the database
    """
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
    """
    Verify user login credentials

    Checks whether a user exists with the provided email and
    validates the provided password against the stored hash

    Args:
        user: UserLogin object containing login credentials
        session: Active database sessio

    Returns:
        existing_user: The authenticated User instance if credentials are valid
        otherwise None
    """
    existing_user = get_user_by_email(user.email, session)
    if existing_user and verify_password(user.password, existing_user.password):
            return existing_user

    return None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]) -> User:
    """
    Retrieve authenticated user from a JWT token

    The token is extracted from the Authorization header using
    the OAuth2 password bearer scheme

    Args:
        token: Token provided in the request header
        session: Active database session

    Returns:
        user: Authenticated User instance

    Raises:
        HTTPException 401: Token is invalid or missing
        HTTPException 404: User does not exist
    """
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

