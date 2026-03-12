"""
User models

Defines models for the User items
- Base fields
- Database table model
- Input models for registration, login and updates
- Public model
"""

from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    """
    Base model for a User item
    """
    email: EmailStr = Field(index = True)

class User(UserBase, table = True):
    """
    Database table model for User

    Inherits from UserBase and adds:
    - id: Primary key
    - name: User's full name
    - password: Hashed password stored in the database
    """
    id: int | None = Field(default = None, primary_key = True, description="Primary key id")
    name: str = Field(index=True, description="Full name of the user")
    password: str

class UserPublic(UserBase):
    """
    Public representation of a User

    Excludes sensitive information such as password
    """
    id: int

class UserLogin(UserBase):
    """
    Model for user login

    Contains email and password fields for authentication
    """
    password: str

class UserCreate(UserBase):
    """
    Model for creating a new user

    Includes all fields needed for registration
    """
    name: str
    password: str

class UserUpdate():
    """
    Model for updating existing user information

    All fields are optional to allow partial updates
    """
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None