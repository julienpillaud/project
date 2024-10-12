from sqlalchemy import select

from app.repository.interface import AbstractSiteRepository
from app.repository.sql.models import Site
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate


class SQLAlchemySiteRepository(
    AbstractSiteRepository,
    SQLAlchemyRepositoryBase[Site, SiteDetail, SiteCreate, SiteUpdate],
):
    model = Site
    schema = SiteDetail

    def get_by_code(self, code: str) -> SiteDetail | None:
        stmt = select(Site).where(Site.code == code)
        entity = self.session.scalars(stmt).first()
        return SiteDetail.model_validate(entity) if entity else None
