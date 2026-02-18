from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

class User(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True)
    name: str = Field(index = True)
    email: str
    password: str

class Todo(SQLModel, table = True):
    id: int | None = Field(default= None, primary_key= True)
    title: str = Field(index = True)
    description : str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]