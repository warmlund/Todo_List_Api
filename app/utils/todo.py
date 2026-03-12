"""
Functions for todo operations

Helper functions for:
    - Creating todo
    - Updating todo
    - Deleting todo
    - Get todo
    - Get multiple todos paginated
"""

from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.todo import Todo, TodoCreate, TodoUpdate

def create_todo_in_db(todo: TodoCreate, session:Session, user_id: int):
    """
    Create and store a new todo in the database

    Args:
        todo: TodoCreate object containing todo data
        session: Active database session
        user_id: Id of authenticated user

    Returns:
        new_todo: Created todo

    Raises:
        HTTPException 400: todo item can't be added to the database

    """
    new_todo =  Todo(title = todo.title, description = todo.description, user_id = user_id)

    try:
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return new_todo
    
    except Exception as e:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Error creating todo: {e}"
        )

def get_existing_todo(todo_id: int, session: Session, user_id: int):
    """
    Get existing todo

    Gets a todo from the database by id and logged in user's id

    Args:
        todo_id: The todo id
        session: The current database session
        user_id: The logged in user's id

    Returns:
        existing_todo: The todo that matches input todo id

    Raises:
        HTTPException 404: No todo items has the input todo id
        HTTPException 403: The input user id is not authorized to get the todo item
    """
    existing_todo = session.get(Todo, todo_id)

    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    
    elif existing_todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to access this todo item")

    return existing_todo

def update_todo_in_db(todo_id: int, todo_update: TodoUpdate, session: Session, user_id: int):
    """
    Update existing todo

    Retrieves existing todo item, applies updated data
    and commits changes to the database

    Args:
        todo_id: Id of the todo item to update
        todo_update: Todo object with updated data
        session: Active database session
        user_id: Id of the authenticated user

    Returns:
        existing_todo: Existing todo with updated data

    Raises:
        HTTPException 400: The update failed
    """
    existing_todo = get_existing_todo(todo_id, session, user_id)

    try:
        update_data = todo_update.model_dump(exclude_unset=True, exclude={"id"})
        update_data["user_id"] = user_id

        existing_todo.sqlmodel_update(update_data)

        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)

        return existing_todo

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating todo: {e}"
        )
    
def delete_todo_in_db(todo_id: int, session: Session, user_id: int):
    """
    Delete todo from the database

    Deletes a todo item from the database if the
    todo item belongs to the authenticated user

    Args:
        todo_id: Id of todo to delete
        session: Active database session
        user_id: Id of authenticated user

    Returns:
        todo: Deleted todo instance

    Raises:
        HTTPException 404: The todo item doesn't exist
        HTTPException 400: Deletion fails
    """
    try:
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = session.exec(statement).one_or_none()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = "Todo item not found"
            )
        
        session.delete(todo)
        session.commit()
        return todo

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f"Error deleting todo: {e}"
        )
    
def get_todos_in_db(session: Session, page: int, limit: int, user_id: int):
    """
    Retrieves todos for a user paginated

    Calculates the correct offset based on requested page
    and returns a limited set of todo items

    Args:
        session: Active database session
        page: Requested page number
        limit: Number of items per page
        user_id: Id of the authenticated user

    Returns:
        Dictionary:
            data: List of todos
            page: Current page number
            limit: Items per page
            total: Number of todos returned

    Raises:
        HTTPException 404: Todos can't be retrieved
    """
    try:
        offset = (page-1)*limit
        statement = select(Todo).where(Todo.user_id == user_id).offset(offset).limit(limit)
        todos = session.exec(statement).all()

        return {"data": todos,
                "page": page,
                "limit": limit,
                "total": len(todos)}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Todo items not found: {e}"
        )