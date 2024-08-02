import uuid

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    upn: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    upn: str
    first_name: str
    last_name: str


class UserUpdate(UserBase):
    pass


class UserDetail(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    upn: str
    first_name: str
    last_name: str
