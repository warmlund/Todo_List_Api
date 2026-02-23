from fastapi import APIRouter
from app.models.todo import Todo, TodoCreate
from app.db import SessionDep

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/todos")
def create(todo: TodoCreate, session: SessionDep) -> Todo:
    new_todo = Todo(**todo.model_dump())
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

#TODO edit endpoint for verifying user token and getting user from token
#TODO: test endpoint with creating todo and verify that it returns correct information
# TODO: add enpoint for updating todo item
#TODO: add endpoint for deleting todo item
#TODO: add endpoint for getting all todo items for a user