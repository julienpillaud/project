from sqlalchemy.orm import Session

from app.users.models import User

from .utils import random_email, random_string


def create_user(session: Session) -> User:
    entity = User(
        upn=random_email(),
        first_name=random_string(),
        last_name=random_string(),
    )
    session.add(entity)
    session.commit()
    return entity
