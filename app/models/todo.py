from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: str = Field(index=True)

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
    pass

class TodoUpdate():
    title: str | None = None
    description: str | None = None