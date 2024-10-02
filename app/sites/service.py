import uuid

from app.repository.interface import AbstractSiteRepository
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate


class SiteService:
    def __init__(self, repository: AbstractSiteRepository):
        self.repository = repository

    def get_sites(self) -> list[SiteDetail]:
        return self.repository.get_all()

    def get_site(self, site_id: uuid.UUID) -> SiteDetail | None:
        return self.repository.get(entity_id=site_id)

    def get_site_by_code(self, code: str) -> SiteDetail | None:
        return self.repository.get_by_code(code)

    def create_site(self, site_create: SiteCreate) -> SiteDetail:
        return self.repository.create(entity_create=site_create)

    def update_site(self, site_id: uuid.UUID, site_update: SiteUpdate) -> SiteDetail:
        return self.repository.update(entity_id=site_id, entity_update=site_update)

    def delete_site(self, site_id: uuid.UUID) -> None:
        self.repository.delete(entity_id=site_id)
