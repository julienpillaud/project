from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    code: str
    description: str


class RoleUpdate(BaseModel):
    description: str


class RoleDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    description: str
