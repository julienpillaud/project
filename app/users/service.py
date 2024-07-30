from app.repository.interface import AbstractRepository
from app.users.schemas import UserCreate, UserDetail, UserUpdate


class UserService:
    @staticmethod
    def get_users(repository: AbstractRepository[UserDetail]) -> list[UserDetail]:
        return repository.get_all()

    @staticmethod
    def get_user(
        repository: AbstractRepository[UserDetail], user_id: int
    ) -> UserDetail | None:
        return repository.get(entity_id=user_id)

    @staticmethod
    def create_user(
        repository: AbstractRepository[UserDetail], user_create: UserCreate
    ) -> UserDetail:
        return repository.create(entity_create=user_create.model_dump())

    @staticmethod
    def update_user(
        repository: AbstractRepository[UserDetail],
        user_id: int,
        user_update: UserUpdate,
    ) -> UserDetail | None:
        return repository.update(
            entity_id=user_id, entity_update=user_update.model_dump()
        )

    @staticmethod
    def delete_user(repository: AbstractRepository[UserDetail], user_id: int) -> None:
        return repository.delete(entity_id=user_id)
