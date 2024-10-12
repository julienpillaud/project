from pydantic import BaseModel, ConfigDict

from app.entities import BaseEntity


class RoleCreate(BaseModel):
    code: str
    description: str


class RoleUpdate(BaseModel):
    description: str


class RoleDetail(BaseEntity):
    model_config = ConfigDict(from_attributes=True)

    code: str
    description: str
