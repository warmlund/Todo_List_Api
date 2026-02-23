from pydantic import EmailStr
from sqlmodel import Session, select

from fastapi import HTTPException, status, Depends
from fastapi import security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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

    if not existing_user:
        return None
    
    if verify_password(user.password, existing_user.password):
        return existing_user
        
    return None

def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)) -> User:
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_user_token(token)
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except:
        raise credentials_exception
    
    statement = select(User).where(User.id == int(user_id))
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception

    return user

