import uuid

from sqlalchemy.orm import Session

from app.repository.sqlalchemy.models import Site, User

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


def add_site_to_user(session: Session, user: User, site: Site) -> User:
    user.sites.append(site)
    session.commit()
    return user


def get_user(session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)
