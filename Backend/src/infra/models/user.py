from typing import Optional

from pydantic import BaseModel, Field

from ...helpers.generalHelpers import PyObjectId


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    password: str
    name: str
    calendar: list[str]
    preferences: list[str] = []
    groups: list[str] = []


class UserForGroup(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    calendar: list[str]
    preferences: list[str] = []


class UserAuth(BaseModel):
    name: str
    password: str
