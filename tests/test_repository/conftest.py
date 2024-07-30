from typing import Any, Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.repository.inmemory_repo import AbstractInMemoryRepository
from app.repository.sqlalchemy_repo import Base
from app.users.models import User, UserSQLRepository
from app.users.schemas import UserDetail


class UserInMemoryRepository(AbstractInMemoryRepository[UserDetail]):
    """Implement an in-memory repository with UserDetail schema."""

    def __init__(self, input_data: list[dict[str, Any]]) -> None:
        self.entity = UserDetail
        self.key = "id"
        self.fake_data = [self.entity.model_validate(data) for data in input_data]


@pytest.fixture()
def user_inmemory_repo(session: Session) -> UserInMemoryRepository:
    input_data: list[dict[str, Any]] = [
        {"id": 1, "name": "user 1"},
        {"id": 2, "name": "user 2"},
    ]
    return UserInMemoryRepository(input_data=input_data)


@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as sql_session:
        user_1 = User(id=1, name="user 1")
        user_2 = User(id=2, name="user 2")
        sql_session.add(user_1)
        sql_session.add(user_2)
        sql_session.commit()
        yield sql_session


@pytest.fixture()
def user_sqlalchemy_repo(session: Session) -> UserSQLRepository:
    return UserSQLRepository(session=session)
