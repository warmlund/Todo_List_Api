"""
Todo models

Defines models for Todo items
- Base fields
- Database table model
- Input models for creation and update
"""

from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    """
    Base model for a Todo item
    """
    title: str = Field(index=True, description="Title of the todo item")
    description: str = Field(index=True, description="Description of the todo item")
    

class Todo(TodoBase, table=True):
    """
    Todo database table model

    Inherits from TodoBase and adds:
    - user_id: Foreign key linking the todo to a user
    - id: Primary key of the todo
    """
    user_id: int = Field(default=None, foreign_key="user.id", description="Id of the user who owns the todo")
    id: int | None = Field(default=None, primary_key=True, description="Primary key id of the todo")

class TodoCreate(TodoBase):
    """
    Model for creating a new todo item

    Inherits from TodoBase, all fields required for creation
    """
    pass

class TodoUpdate(SQLModel):
    """
    Model for updating an existing todo item

    Fields are optional, allowing partial updates
    """
    title: str | None = None
    description: str | None = None