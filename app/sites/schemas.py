import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

SiteCode = Annotated[str, StringConstraints(to_upper=True, max_length=4)]


class SiteCreate(BaseModel):
    code: SiteCode
    name: str


class SiteUpdate(BaseModel):
    name: str


class SiteDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code: SiteCode
    name: str
