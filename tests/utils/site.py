from sqlalchemy.orm import Session

from app.sites.models import Site

from .utils import random_string


def create_site(session: Session) -> Site:
    entity = Site(code=random_string(size=4, upper=True), name=random_string())
    session.add(entity)
    session.commit()
    return entity
