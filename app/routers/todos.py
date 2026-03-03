from fastapi import APIRouter, Depends, Query
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
    deleted_todo = delete_todo_in_db(todo_id, session, current_user.id)
    return deleted_todo

@router.get("/gettodos")
def read_todos(session: SessionDep, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), current_user = Depends(get_current_user)):
    todos = get_todos_in_db(session, page, limit, current_user.id)
    return todos