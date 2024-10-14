import uuid
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

ServiceName = Literal["role", "site", "user"]


class DatabaseType(StrEnum):
    INMEMORY = "inmemory"
    SQLALCHEMY = "sqlalchemy"


class BaseEntity(BaseModel):
    id: uuid.UUID
