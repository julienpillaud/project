import uuid

from pydantic import BaseModel, ConfigDict

from app.sites.schemas import SiteDetail


class UserCreate(BaseModel):
    upn: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    pass


class UserDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    upn: str
    first_name: str
    last_name: str

    sites: list[SiteDetail]
