import uuid
from typing import Any

from sqlalchemy import delete, select

from app.repository.interface import AbstractUserRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.users.models import User
from app.users.schemas import UserDetail


class SQLAlchemyUserRepository(
    SQLAlchemyRepositoryBase[User, UserDetail], AbstractUserRepository
):
    model = User
    schema = UserDetail

    def get(self, entity_id: uuid.UUID) -> UserDetail | None:
        stmt = select(User).where(User.id == entity_id)
        model_obj = self.session.scalars(stmt).first()
        return UserDetail.model_validate(model_obj) if model_obj else None

    def get_by_upn(self, upn: str) -> UserDetail | None:
        stmt = select(User).where(User.upn == upn)
        model_obj = self.session.scalars(stmt).first()
        return UserDetail.model_validate(model_obj) if model_obj else None

    def delete(self, entity_id: uuid.UUID) -> None:
        stmt = delete(User).where(User.id == entity_id)
        self.session.execute(stmt)


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self, data: list[UserDetail]) -> None:
        self.data = data

    def get_all(self) -> list[UserDetail]:
        return self.data

    def get(self, entity_id: uuid.UUID) -> UserDetail | None:
        return next((item for item in self.data if item.id == entity_id), None)

    def get_by_upn(self, upn: str) -> UserDetail | None:
        return next((item for item in self.data if item.upn == upn), None)

    def create(self, entity_create: dict[str, Any]) -> UserDetail:
        entity_create["id"] = uuid.uuid4()
        data = UserDetail.model_validate(entity_create)
        self.data.append(data)
        return data

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]
