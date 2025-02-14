import os
from os.path import dirname, join

from dotenv import load_dotenv
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), ".env")
load_dotenv()

mongodb_url = os.getenv("DATABASE_URL")

assert mongodb_url != None, "Database connection string not found"
assert isinstance(mongodb_url, str), "Database connection string is not valid"

client = MongoClient(mongodb_url)
assert isinstance(client, MongoClient), "Could not find database"


def get_test_db():
    db = client["test_db"]
    try:
        yield db
    finally:
        pass
