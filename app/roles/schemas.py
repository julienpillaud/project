import uuid

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    code: str | None = None
    description: str | None = None


class RoleCreate(RoleBase):
    code: str
    description: str


class RoleUpdate(RoleBase):
    pass


class RoleDetail(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
