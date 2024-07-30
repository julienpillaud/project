from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str | None = None
    username: str | None = None


class UserCreate(UserBase):
    email: str
    username: str


class UserUpdate(UserBase):
    pass


class UserDetail(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
