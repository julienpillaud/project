import uuid
from typing import Any

from sqlalchemy import select

from app.repository.interface import AbstractUserRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.sites.models import Site
from app.users.models import User
from app.users.schemas import UserDetail


class SQLAlchemyUserRepository(
    SQLAlchemyRepositoryBase[User, UserDetail], AbstractUserRepository
):
    model = User
    schema = UserDetail

    def get_by_upn(self, upn: str) -> UserDetail | None:
        stmt = select(User).where(User.upn == upn)
        model_obj = self.session.scalars(stmt).first()
        return UserDetail.model_validate(model_obj) if model_obj else None

    def add_site_to_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> UserDetail:
        user = self.session.get(User, user_id)
        site = self.session.get(Site, site_id)
        if not user or not site:
            raise ValueError
        user.sites.append(site)
        self.session.commit()
        return UserDetail.model_validate(user)

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None:
        user = self.session.get(User, user_id)
        site = self.session.get(Site, site_id)
        if not user or not site:
            raise ValueError
        user.sites.remove(site)
        self.session.commit()


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
        entity_create["sites"] = []
        data = UserDetail.model_validate(entity_create)
        self.data.append(data)
        return data

    def update(self, entity_id: uuid.UUID, entity_update: dict[str, Any]) -> UserDetail:
        return NotImplemented

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]

    def add_site_to_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> UserDetail:
        return NotImplemented

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None:
        return None
