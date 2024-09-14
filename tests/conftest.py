import uuid
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.main import app
from app.repository.interface import Base
from app.repository.role_repositpry import InMemoryRoleRepository
from app.repository.site_repositpry import InMemorySiteRepository
from app.repository.user_repository import InMemoryUserRepository
from app.roles.schemas import RoleDetail
from app.sites.schemas import SiteDetail
from app.users.schemas import UserDetail


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Iterator[TestClient]:
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


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
        ),
        UserDetail(
            id=uuid.uuid4(),
            upn="user2@mail.com",
            first_name="user 2",
            last_name="",
        ),
    ]
    return InMemoryUserRepository(data=data)
