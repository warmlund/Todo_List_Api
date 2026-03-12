# Todo List API
> A simple API built with FastAPI. The API manages:
> - User registration, authentication, and login
> - Creating, updating, deleting, and retrieving todo items

## Table of Contents
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Contact](#contact)

## General Information
- This is a RESTful API to manage Todo items for authenticated users.
- Built with a three-tier architecture: Database, API, and optional frontend.
- Supports CRUD operations (Create, Read, Update, Delete) for todo items.
- Uses JWT authentication for secure user sessions.

## Technologies Used
- **Programming Language:** Python 3.11+
- **Backend Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLModel
- **Authentication:** OAuth2 / JWT
- **Testing:** Pytest, FastAPI TestClient

## Features
- **User Management**
  - Register a new user
  - Login and receive JWT token
  - Retrieve all users (protected route)
- **Todo Management**
  - Create a todo item (authenticated users only)
  - Retrieve paginated todos
  - Update existing todos
  - Delete todos
- **Security**
  - Password hashing with bcrypt
  - Token-based authentication
  - User-specific access to todos
