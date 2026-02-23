from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate, UserLogin
from app.db import SessionDep
from app.utils.user import *
from app.utils.token import create_user_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/registration")
def register(user: UserCreate, session: SessionDep):
    
    existing_user = get_user_by_email(user.email, session)

    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already registered")
    
    new_user = create_user_in_db(user, session)
    token = create_user_token(new_user)
    return token

@router.post("/login")
def login(user: UserLogin, session: SessionDep):

    existing_user = verify_login(user, session)

    if not existing_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid login credentials")
        
    token = create_user_token(existing_user)
    return {"access_token": token, "token_type": "bearer"}

#TODO: Add endpoint to get user from token