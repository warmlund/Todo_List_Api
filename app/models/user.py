from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(index = True)

class User(UserBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    name: str = Field(index=True)
    password: str

class UserPublic(UserBase):
    id: int

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    name: str
    password: str

class UserUpdate():
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
