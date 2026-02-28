from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.todo import Todo, TodoCreate

def create_todo_in_db(todo: TodoCreate, session:Session):
   
    new_todo =  Todo(title = todo.title, description = todo.description)

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