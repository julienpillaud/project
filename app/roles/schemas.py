import uuid

from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    code: str
    description: str


class RoleUpdate(BaseModel):
    description: str


class RoleDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: str
    description: str
