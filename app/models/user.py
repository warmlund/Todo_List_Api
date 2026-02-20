from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr = Field(index = True)

class User(UserBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    password: bytes

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserUpdate():
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
