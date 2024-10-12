from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from app.entities import BaseEntity

SiteCode = Annotated[str, StringConstraints(to_upper=True, max_length=4)]


class SiteCreate(BaseModel):
    code: SiteCode
    name: str


class SiteUpdate(BaseModel):
    name: str


class SiteDetail(BaseEntity):
    model_config = ConfigDict(from_attributes=True)

    code: SiteCode
    name: str
