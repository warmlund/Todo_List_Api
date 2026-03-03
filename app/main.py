from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.todos import router as todo_router

from app.db import create_db_and_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan = lifespan)
    app.include_router(users_router)
    app.include_router(todo_router)

    return app

app = create_app()