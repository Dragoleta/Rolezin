import os
from datetime import datetime, timedelta
from os.path import dirname, join

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..infra.models.auth_token import AuthToken

auth_router = APIRouter()

dotenv_path = join(dirname(__file__), ".env")
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


async def generate_token(user_name: str, user_id: str):
    expires_delta = int(os.environ.get("TOKEN_EXPIRATION_LIMIT"))

    encode = {"sub": user_id, "name": user_name}
    expires = datetime.utcnow() + timedelta(minutes=expires_delta)
    encode.update({"exp": expires})

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


async def check_user_token(authToken: AuthToken = Depends(oauth2_scheme)):

    token_bytes = authToken.encode("utf-8")
    payload = jwt.decode(token_bytes, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    user_name = payload.get("name")

    if user_name is None or user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id, user_name
