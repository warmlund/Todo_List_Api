from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.models.user import User
from app.db import SessionDep

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/registration")
def register(user: UserCreate, session: SessionDep) -> User:
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user