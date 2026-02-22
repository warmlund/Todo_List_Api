import bcrypt

from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserLogin
from pydantic import EmailStr

def hash_password(password: str) -> str:
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(pw, salt)

    return hash.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    check_pw = bcrypt.checkpw(password.encode("utf-8"),
                              hashed_password.encode("utf-8")
                              )
    
    return check_pw

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
