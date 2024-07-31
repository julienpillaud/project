import uuid
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
        user_1 = User(
            id=uuid.uuid4(), upn="user1@mail.com", first_name="user 1", last_name=""
        )
        user_2 = User(
            id=uuid.uuid4(), upn="user2@mail.com", first_name="user 2", last_name=""
        )
        sql_session.add(user_1)
        sql_session.add(user_2)
        sql_session.commit()
        yield sql_session


@pytest.fixture()
def user_sqlalchemy_repo(session: Session) -> UserSQLRepository:
    return UserSQLRepository(session=session)
