import uuid

from app.repository.interface import AbstractUserRepository
from app.users.schemas import UserCreate, UserDetail


class UserService:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    def get_users(self) -> list[UserDetail]:
        return self.repository.get_all()

    def get_user(self, user_id: uuid.UUID) -> UserDetail | None:
        return self.repository.get(entity_id=user_id)

    def get_user_by_upn(self, upn: str) -> UserDetail | None:
        return self.repository.get_by_upn(upn=upn)

    def create_user(self, user_create: UserCreate) -> UserDetail:
        return self.repository.create(entity_create=user_create.model_dump())

    def delete_user(self, user_id: uuid.UUID) -> None:
        self.repository.delete(entity_id=user_id)
