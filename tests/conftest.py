import uuid

import pytest

from app.repository.role_repositpry import InMemoryRoleRepository
from app.repository.user_repository import InMemoryUserRepository
from app.roles.schemas import RoleDetail
from app.users.schemas import UserDetail


@pytest.fixture
def user_repository() -> InMemoryUserRepository:
    data = [
        UserDetail(
            id=uuid.uuid4(),
            upn="user1@mail.com",
            first_name="user 1",
            last_name="",
        ),
        UserDetail(
            id=uuid.uuid4(),
            upn="user2@mail.com",
            first_name="user 2",
            last_name="",
        ),
    ]
    return InMemoryUserRepository(data=data)


@pytest.fixture
def role_repository() -> InMemoryRoleRepository:
    data = [
        RoleDetail(
            id=uuid.uuid4(),
            code="DEV",
            description="",
        ),
        RoleDetail(
            id=uuid.uuid4(),
            code="ADMIN",
            description="",
        ),
    ]
    return InMemoryRoleRepository(data=data)
