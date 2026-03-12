"""
OAuth2 authentication configuration

Deifines the OAUth2 password bearer scheme used to extract
JWT tokens from the Authorization header
"""

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")