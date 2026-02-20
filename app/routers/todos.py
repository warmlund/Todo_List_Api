from fastapi import APIRouter
from app.schemas.todo import TodoCreate
from app.models.todo import Todo
from app.db import SessionDep

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/create")
def create(todo: TodoCreate, session: SessionDep) -> Todo:
    new_todo = Todo(**todo.model_dump())
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo