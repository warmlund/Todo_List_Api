from fastapi import APIRouter
from app.models.todo import Todo, TodoCreate
from app.db import SessionDep
from app.utils.todo import create_todo_in_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/todos", response_model=Todo)
def create(todo: TodoCreate, session: SessionDep):
    new_todo = create_todo_in_db(todo, session)
    return new_todo

#TODO edit endpoint for verifying user token and getting user from token
#TODO: test endpoint with creating todo and verify that it returns correct information
# TODO: add enpoint for updating todo item
#TODO: add endpoint for deleting todo item
#TODO: add endpoint for getting all todo items for a user