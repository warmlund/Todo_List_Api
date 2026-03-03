from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(index=True)
    

class Todo(TodoBase, table=True):

    user_id: int = Field(default=None, foreign_key="user.id")
    id: int | None = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None