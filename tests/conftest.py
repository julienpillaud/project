import uuid

import pytest

from app.repository.role_repositpry import InMemoryRoleRepository
from app.repository.site_repositpry import InMemorySiteRepository
from app.repository.user_repository import InMemoryUserRepository
from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail


@pytest.fixture
def role_repository() -> InMemoryRoleRepository:
    data = [
        RoleDetail(code="DEV", description="developer"),
        RoleDetail(code="ADMIN", description="administrator"),
    ]
    return InMemoryRoleRepository(data=data)


@pytest.fixture
def site_repository() -> InMemorySiteRepository:
    data = [
        SiteDetail(code="SITE1", name="site 1"),
        SiteDetail(code="SITE2", name="site2"),
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
        ),
        UserDetail(
            id=uuid.uuid4(),
            upn="user2@mail.com",
            first_name="user 2",
            last_name="",
        ),
    ]
    return InMemoryUserRepository(data=data)
