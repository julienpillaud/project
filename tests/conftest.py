import uuid
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
        {
            "id": uuid.uuid4(),
            "upn": "user1@mail.com",
            "first_name": "user 1",
            "last_name": "",
        },
        {
            "id": uuid.uuid4(),
            "upn": "user2@mail.com",
            "first_name": "user 2",
            "last_name": "",
        },
    ]
    return UserInMemoryRepository(input_data=input_data)
