import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app
from app.utils.user import create_user_in_db
from app.utils.todo import create_todo_in_db
from app.utils.token import create_user_token
from app.models.user import UserCreate
from app.models.todo import TodoCreate

"""
Shared pytest fixtures for API unit tests

- test database
- FastAPI TestClient
- test user, todo and auhentication token
"""

# ------------------------------------------------------------------
# Test Database Configuration
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def engine():
    """
    Creates a database for the test session

    StaticPool ensueres the same database connection is reused
    across multiple sessions during testing
    """
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    return engine


# ------------------------------------------------------------------
# Test Database Session Fixture
# ------------------------------------------------------------------

@pytest.fixture
def session(engine):
    """
    Provides a database session for each test

    A new session is created and closed after
    test finishes
    """
    with Session(engine) as session:
        yield session


# ------------------------------------------------------------------
# FastAPI Test Client
# ------------------------------------------------------------------

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Creates a FatAPI test client with the database dependency overridden
    to instead use the test database
    """
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    # Clean up dependency after test
    app.dependency_overrides.clear()


# ------------------------------------------------------------------
# Test Data Fixtures
# ------------------------------------------------------------------

@pytest.fixture(name="test_user", scope="function")
def test_user_fixture(session: Session):
    """
    Creates a test user
    """
    user_test_data = UserCreate(email="test@example.com", name="Test user", password="password123")
    test_user = create_user_in_db(user_test_data, session)
    return test_user

@pytest.fixture(name="test_todo", scope="function")
def test_todo_fixture(test_user, session: Session):
    """
    Creates a todo item belonging to the test user
    """
    todo_test_data = TodoCreate(title = "Test todo", description = "Test description")
    test_todo = create_todo_in_db(todo_test_data, session, test_user.id)
    return test_todo

@pytest.fixture(name ="test_token", scope ="function")
def test_token_fixture(test_user):
    """
    Generates a JWT token for the test user
    """
    test_token = create_user_token(test_user)
    return test_token

@pytest.fixture
def auth_client(client, test_token):
    """
    Creates authenticated client fixture for test token
    """
    client.headers.update({
        "Authorization": f"Bearer {test_token}"
    })

    return client