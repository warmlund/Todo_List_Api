from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.todo import Todo, TodoCreate, TodoUpdate
from app.db import SessionDep
from app.utils.todo import *
from app.utils.user import get_current_user

router = APIRouter(tags=["todos"])

@router.post("/todos", response_model=Todo)
def create(todo: TodoCreate, session: SessionDep, current_user = Depends(get_current_user)):
    new_todo = create_todo_in_db(todo, session, current_user.id)
    return new_todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update(todo_id: int, todo: TodoUpdate, session: SessionDep, current_user = Depends(get_current_user)):
    updated_todo = update_todo_in_db(todo_id, todo, session, current_user.id)
    return updated_todo

@router.delete("/todos/{todo_id}", status_code=204)
def delete(todo_id:int, session: SessionDep, current_user = Depends(get_current_user)):
    delted_todo = delete_todo_in_db(todo_id, session, current_user.id)
    return delted_todo

@router.get("/gettodos")
def read_todos(session: SessionDep, offset: int = 0, limit: int = 1000):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos

#TODO: add endpoint for deleting todo item
#TODO: add endpoint for getting all todo items for a user