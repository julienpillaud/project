import uuid

from app.repository.inmemory.base import InMemoryRepositoryBase
from app.repository.interface import AbstractUserRepository
from app.users.schemas import UserCreate, UserDetail, UserUpdate


class InMemoryUserRepository(
    AbstractUserRepository, InMemoryRepositoryBase[UserDetail, UserCreate, UserUpdate]
):
    model = UserDetail

    def get_by_upn(self, upn: str) -> UserDetail | None:
        return next((item for item in self.data if item.upn == upn), None)

    def add_site_to_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> UserDetail:
        return NotImplemented

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None:
        return None
