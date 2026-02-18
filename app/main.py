from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.users import router as users_router

from app.db import create_db_and_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan = lifespan)

    app.include_router(users_router)

    return app

app = create_app()