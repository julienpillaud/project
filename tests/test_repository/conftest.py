from typing import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.repository.sqlalchemy_repo import Base
from app.users.models import User, UserSQLRepository


@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as sql_session:
        user_1 = User(id=1, email="user1@mail.com", username="user 1")
        user_2 = User(id=2, email="user2@mail.com", username="user 2")
        sql_session.add(user_1)
        sql_session.add(user_2)
        sql_session.commit()
        yield sql_session


@pytest.fixture()
def user_sqlalchemy_repo(session: Session) -> UserSQLRepository:
    return UserSQLRepository(session=session)
