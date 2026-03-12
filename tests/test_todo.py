from app.models.user import UserCreate
from app.utils.user import create_user_in_db
from app.utils.token import create_user_token

"""
Unit tests for todo-related functionality

Tests:
- correct todo creation is sucessful
- creating todo without authentication fails
- uer can update a todo item
- user can delete a todo item
- user can't access another users todo items
- user can retrieve their todos 
"""

def test_create_todo(auth_client):
    """
    User that is logged in can create a todo
    """

    response = auth_client.post(
        "/todos",
        json = {"title": "Buy groceries", "description": "milk"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Buy groceries"

def test_create_todo_without_auth(client):
    """
    Creating a todo without being logged in
    and having authentication
    """

    response = client.post(
        "/todos",
        json = {"title": "Buy groceries", "description": "milk"}
    )

    assert response.status_code == 401

def test_user_update_todo(auth_client, test_todo):
    """
    User that is logged in can update their todo
    """

    response = auth_client.put(
        f"/todos/{test_todo.id}",
        json={"description": "milk and cereal"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "milk and cereal"

def test_user_get_todos(auth_client, test_todo):
    """
    User can retrieve their todos
    """

    response = auth_client.get(
        "/gettodos"
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) >= 1

def test_delete_todo(auth_client, test_todo):
    """
    User can delete their todo
    """

    response = auth_client.delete(
        f"/todos/{test_todo.id}"
    )

    assert response.status_code == 204

def test_no_access_other_users_todo(client, session, test_todo):
    """
    User can't access another user's todos
    """

    other_user = create_user_in_db(
        UserCreate(
            email = "other@example.com",
            name = "other user",
            password = "password123"
        ),
        session
    )

    other_token = create_user_token(other_user)

    response = client.get(
        f"/todos/{test_todo.id}",
        headers  = {"Authorization": f"Bearer {other_token}"}
    )

    assert response.status_code == 405