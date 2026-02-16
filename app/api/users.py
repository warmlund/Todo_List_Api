from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/registration")
def register(user: UserCreate):
    new_user = User(**user.model_dump())
    return {"name": new_user.name, "email": new_user.email}