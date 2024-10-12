import uuid

import pytest

from app.repository.inmemory.role import InMemoryRoleRepository
from app.repository.inmemory.site import InMemorySiteRepository
from app.repository.inmemory.user import InMemoryUserRepository
from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail


@pytest.fixture
def role_repository() -> InMemoryRoleRepository:
    data = [
        RoleDetail(id=uuid.uuid4(), code="DEV", description="developer"),
        RoleDetail(id=uuid.uuid4(), code="ADMIN", description="administrator"),
    ]
    return InMemoryRoleRepository(data=data)


@pytest.fixture
def site_repository() -> InMemorySiteRepository:
    data = [
        SiteDetail(id=uuid.uuid4(), code="SIT1", name="site 1"),
        SiteDetail(id=uuid.uuid4(), code="SIT2", name="site 2"),
    ]
    return InMemorySiteRepository(data=data)


@pytest.fixture
def user_repository() -> InMemoryUserRepository:
    data = [
        UserDetail(
            id=uuid.uuid4(),
            upn="user1@mail.com",
            first_name="user 1",
            last_name="",
            sites=[],
        ),
        UserDetail(
            id=uuid.uuid4(),
            upn="user2@mail.com",
            first_name="user 2",
            last_name="",
            sites=[],
        ),
    ]
    return InMemoryUserRepository(data=data)
