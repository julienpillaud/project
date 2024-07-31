from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.database import engine


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
