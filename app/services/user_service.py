from app.models.user import User

users = []

def create_user(name: str, email: str, password: str) -> User:
    user = User(name = name, email = email, password = password)
    users.append(user)
    return user