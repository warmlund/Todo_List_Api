from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserLogin
from app.db import SessionDep
from app.utils.user import *
from app.utils.token import create_user_token

router = APIRouter(tags=["users"])

@router.post("/register")
def register(user: UserCreate, session: SessionDep):
    
    existing_user = get_user_by_email(user.email, session)

    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already registered")
    
    new_user = create_user_in_db(user, session)
    token = create_user_token(new_user)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[SessionDep, Depends(get_session)]):

    existing_user = verify_login(UserLogin(email=form_data.username, password=form_data.password), session)

    if not existing_user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid login credentials")
        
    token = create_user_token(existing_user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/getusers")
def read_users(session: SessionDep, offset: int = 0, limit: int = 1000):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users