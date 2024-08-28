from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.repository.interface import AbstractSiteRepository
from app.sites.models import Site
from app.sites.schemas import SiteDetail


class SQLAlchemySiteRepository(AbstractSiteRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[SiteDetail]:
        stmt = select(Site)
        entities = self.session.scalars(stmt)
        return [SiteDetail.model_validate(entity) for entity in entities]

    def get_by_code(self, code: str) -> SiteDetail | None:
        stmt = select(Site).where(Site.code == code)
        entity = self.session.scalars(stmt).first()
        return SiteDetail.model_validate(entity) if entity else None

    def create(self, entity_create: dict[str, Any]) -> SiteDetail:
        entity = Site(**entity_create)
        self.session.add(entity)
        self.session.commit()
        return SiteDetail.model_validate(entity)

    def update(self, code: str, entity_update: dict[str, Any]) -> SiteDetail:
        stmt = select(Site).where(Site.code == code)
        entity = self.session.scalars(stmt).one()
        for key, value in entity_update.items():
            setattr(entity, key, value)
        self.session.commit()
        return SiteDetail.model_validate(entity)

    def delete(self, code: str) -> None:
        stmt = delete(Site).where(Site.code == code)
        self.session.execute(stmt)
        self.session.commit()


class InMemorySiteRepository(AbstractSiteRepository):
    def __init__(self, data: list[SiteDetail]) -> None:
        self.data = data

    def get_all(self) -> list[SiteDetail]:
        return [SiteDetail.model_validate(entity) for entity in self.data]

    def get_by_code(self, code: str) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)

    def create(self, entity_create: dict[str, Any]) -> SiteDetail:
        data = SiteDetail.model_validate(entity_create)
        self.data.append(data)
        return data

    def update(self, code: str, entity_update: dict[str, Any]) -> SiteDetail:
        entity = self.get_by_code(code=code)
        if not entity:
            raise ValueError

        for key, value in entity_update.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        return entity

    def delete(self, code: str) -> None:
        self.data = [item for item in self.data if item.code != code]
