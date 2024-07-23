from pydantic import ConfigDict

from app.repository.interface import GenericBaseModel


class UserDetail(GenericBaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
