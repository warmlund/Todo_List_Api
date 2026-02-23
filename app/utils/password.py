import bcrypt

def hash_password(password: str) -> str:
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(pw, salt)

    return hash.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    check_pw = bcrypt.checkpw(password.encode("utf-8"),
                              hashed_password.encode("utf-8")
                              )
    
    return check_pw