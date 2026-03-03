from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import HTTPException, status, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models.todo import Todo, TodoCreate, TodoUpdate

def create_todo_in_db(todo: TodoCreate, session:Session, user_id: int):
   
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
    existing_todo = session.get(Todo, todo_id)

    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    
    elif existing_todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to access this todo item")

    return existing_todo

def update_todo_in_db(todo_id: int, todo_update: TodoUpdate, session: Session, user_id: int):
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
    
    try:
        statement = select(Todo).where(Todo.id == todo_id and Todo.user_id == user_id)
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