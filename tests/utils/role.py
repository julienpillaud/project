from sqlalchemy.orm import Session

from app.repository.sql.models import Role

from .utils import random_string


def create_role(session: Session) -> Role:
    entity = Role(code=random_string(upper=True), description=random_string())
    session.add(entity)
    session.commit()
    return entity
