from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    user_id: int = Field(default=None, foreign_key="user.id")
    

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)

class TodoCreate(Todo):
    pass

class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None