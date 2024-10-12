from pydantic import BaseModel, ConfigDict

from app.entities import BaseEntity
from app.sites.schemas import SiteDetail


class UserCreate(BaseModel):
    upn: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    pass


class UserDetail(BaseEntity):
    model_config = ConfigDict(from_attributes=True)

    upn: str
    first_name: str
    last_name: str

    sites: list[SiteDetail] = []
