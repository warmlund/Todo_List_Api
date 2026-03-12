"""
Todo API routes

Defines endpoints for:
    - Creating
    - Updating
    - Deleting
    - Retrieving
"""

from fastapi import APIRouter, Depends, Query
from app.models.todo import Todo, TodoCreate, TodoUpdate
from app.db import SessionDep
from app.utils.todo import *
from app.utils.user import get_current_user

router = APIRouter(tags=["todos"])

@router.post("/todos", response_model=Todo)
def create(todo: TodoCreate, session: SessionDep, current_user = Depends(get_current_user)):
    """
    Create a new todo item

    Args:
        todo: TodoCreate object containing todo data
        session: Active database session
        current_user: Authenticated user retrieved from the JWT token

    Returns:
        new_todo: created todo item
    """
    new_todo = create_todo_in_db(todo, session, current_user.id)
    return new_todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update(todo_id: int, todo: TodoUpdate, session: SessionDep, current_user = Depends(get_current_user)):
    """
    Update an existing todo item

    Args:
        todo_id: Id of the todo item to update
        todo: TodoUpdate object containing updated fields
        session: Active database session
        current_user: Authenticated user retrieved from the JWT token

    Returns:
        updated_todo: Updated Todo item
    """
    updated_todo = update_todo_in_db(todo_id, todo, session, current_user.id)
    return updated_todo

@router.delete("/todos/{todo_id}", status_code=204)
def delete(todo_id:int, session: SessionDep, current_user = Depends(get_current_user)):
    """
    Delete todo item

    Args:
        todo_id: Id of the todo item to delete
        session: Active database session
        current_user: Authenticated user retrieved from the JWT token

    Returns:
        HTTP 204 on successful deletion
    """
    deleted_todo = delete_todo_in_db(todo_id, session, current_user.id)
    return deleted_todo

@router.get("/gettodos")
def read_todos(session: SessionDep, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), current_user = Depends(get_current_user)):
    """
    Retrieve paginated todos for the authenticated user

    Args:
        session: Active database session
        page: Page number for pagination (must be >= 1)
        limit: Number of items per page (1–100)
        current_user: Authenticated user retrieved from the JWT token

    Returns:
        A paginated list of todos
    """
    todos = get_todos_in_db(session, page, limit, current_user.id)
    return todos