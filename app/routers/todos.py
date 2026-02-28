from fastapi import APIRouter, HTTPException, status, Depends
from app.models.todo import Todo, TodoCreate
from app.db import SessionDep
from app.utils.todo import create_todo_in_db
from app.utils.user import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/todos", response_model=Todo)
def create(todo: TodoCreate, session: SessionDep, current_user = Depends(get_current_user)):
    new_todo = create_todo_in_db(todo, session)
    return new_todo

#TODO edit endpoint for verifying user token and getting user from token - now todo items are not linked to any user, 
# so we can create todo items without authentication, but in the future we will link todo items to users and then we will 
# need to verify user token and get user from token before creating todo item
#TODO: test endpoint with creating todo and verify that it returns correct information
# TODO: add enpoint for updating todo item
#TODO: add endpoint for deleting todo item
#TODO: add endpoint for getting all todo items for a user