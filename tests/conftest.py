import pytest
from pydantic import EmailStr
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app import main
from app.db import get_session
from app.main import app
from app.utils.user import create_user_in_db
from app.models.user import UserCreate


@pytest.fixture(scope="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="test_user", scope="function")
def test_user_fixture(override_session):
    user_test_data = UserCreate(email="test@example.com", name="Test user", password="password123")
    test_user = create_user_in_db(user_test_data, override_session)
    return test_user