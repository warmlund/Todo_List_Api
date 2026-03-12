"""
Password encrypt and decrypt utilities

Provides functions for hashing plaintext passwords using bcrypt
and verifying plaintext password against stored bcrypot hash
"""

import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes string password using bcrypt

    Args:
        password: user plaintext password

    Returns:
        hashed password as a UTF-8 encoded string 
    """
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)

    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a stored bcrypt hash

    Args:
        password: Plaintext password provided by the user
        hashed_password: Hashed password stored in the database

    Returns:
        True if password matches stored hash, else False
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))