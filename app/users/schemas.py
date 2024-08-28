import uuid

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    upn: str
    first_name: str
    last_name: str


class UserDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    upn: str
    first_name: str
    last_name: str
