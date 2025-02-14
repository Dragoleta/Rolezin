from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel


class Success(BaseModel):
    code: int
    data: Any


@dataclass
class Failure:
    code: int
    data: str = "Unknown error"
