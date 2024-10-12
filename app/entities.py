import uuid

from pydantic import BaseModel


class BaseEntity(BaseModel):
    id: uuid.UUID
