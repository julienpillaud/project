import uuid

from sqlalchemy import select

from app.repository.interface import AbstractUserRepository
from app.repository.sqlalchemy.base import SQLAlchemyRepositoryBase
from app.repository.sqlalchemy.models import Site, User
from app.users.schemas import UserCreate, UserDetail, UserUpdate


class SQLAlchemyUserRepository(
    AbstractUserRepository,
    SQLAlchemyRepositoryBase[User, UserDetail, UserUpdate, UserCreate],
):
    model = User
    schema = UserDetail

    def get_by_upn(self, upn: str) -> UserDetail | None:
        stmt = select(User).where(User.upn == upn)
        model_obj = self.session.scalars(stmt).first()
        return UserDetail.model_validate(model_obj) if model_obj else None

    def add_site_to_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> UserDetail:
        user = self.session.get(User, user_id)
        site = self.session.get(Site, site_id)
        if not user or not site:
            raise ValueError
        user.sites.append(site)
        self.session.commit()
        return UserDetail.model_validate(user)

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None:
        user = self.session.get(User, user_id)
        site = self.session.get(Site, site_id)
        if not user or not site:
            raise ValueError
        user.sites.remove(site)
        self.session.commit()
