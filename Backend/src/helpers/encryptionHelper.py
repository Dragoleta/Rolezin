import os
from datetime import datetime, timedelta
from os.path import dirname, join

import bcrypt
from dotenv import load_dotenv

# from cryptography.fernet import Fernet

# def get_secret_key():
#     dotenv_path = join(dirname(__file__), ".env")
#     load_dotenv(dotenv_path)

#     SECRET_KEY = os.environ.get("FERNET_KEY")
#     return Fernet(SECRET_KEY.encode("utf-8"))


def hash_password(plain_password: str):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hash_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception as exc:
        print(exc)
