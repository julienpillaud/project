from typing import Any

import pytest

from app.repository.inmemory_repo import AbstractInMemoryRepository
from app.users.schemas import UserDetail


class UserInMemoryRepository(AbstractInMemoryRepository[UserDetail]):
    """Implement an in-memory repository with UserDetail schema."""

    def __init__(self, input_data: list[dict[str, Any]]) -> None:
        self.entity = UserDetail
        self.key = "id"
        self.fake_data = [self.entity.model_validate(data) for data in input_data]


@pytest.fixture()
def user_inmemory_repo() -> UserInMemoryRepository:
    input_data: list[dict[str, Any]] = [
        {"id": 1, "email": "user1@mail.com", "username": "user 1"},
        {"id": 2, "email": "user2@mail.com", "username": "user 2"},
    ]
    return UserInMemoryRepository(input_data=input_data)
