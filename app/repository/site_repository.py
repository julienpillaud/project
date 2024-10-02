import uuid

from sqlalchemy import select

from app.repository.interface import AbstractSiteRepository
from app.repository.sqlalchemy_repository import SQLAlchemyRepositoryBase
from app.sites.models import Site
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate


class SQLAlchemySiteRepository(
    SQLAlchemyRepositoryBase[Site, SiteDetail], AbstractSiteRepository
):
    model = Site
    schema = SiteDetail

    def get_by_code(self, code: str) -> SiteDetail | None:
        stmt = select(Site).where(Site.code == code)
        entity = self.session.scalars(stmt).first()
        return SiteDetail.model_validate(entity) if entity else None


class InMemorySiteRepository(AbstractSiteRepository):
    def __init__(self, data: list[SiteDetail]) -> None:
        self.data = data

    def get_all(self) -> list[SiteDetail]:
        return [SiteDetail.model_validate(entity) for entity in self.data]

    def get(self, entity_id: uuid.UUID) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.id == entity_id), None)

    def get_by_code(self, code: str) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)

    def create(self, entity_create: SiteCreate) -> SiteDetail:
        data = SiteDetail(id=uuid.uuid4(), **entity_create.model_dump())
        self.data.append(data)
        return data

    def update(self, entity_id: uuid.UUID, entity_update: SiteUpdate) -> SiteDetail:
        entity = self.get(entity_id=entity_id)
        if not entity:
            raise ValueError

        for key, value in entity_update.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)

        return entity

    def delete(self, entity_id: uuid.UUID) -> None:
        self.data = [item for item in self.data if item.id != entity_id]
