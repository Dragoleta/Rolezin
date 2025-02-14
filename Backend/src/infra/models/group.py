from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ...helpers.generalHelpers import PyObjectId, generateCode
from ..models.user import UserModel


class GroupModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    code: str = ""
    participants: Optional[list[UserModel]] = []
    calendar: None
    roles: list[str] = []
    rolesOPT: list[int] = []
