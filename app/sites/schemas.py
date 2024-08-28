from pydantic import BaseModel, ConfigDict


class SiteCreate(BaseModel):
    code: str
    name: str


class SiteUpdate(BaseModel):
    name: str


class SiteDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
