from app.repository.interface import AbstractSiteRepository
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate


class SiteService:
    def __init__(self, repository: AbstractSiteRepository):
        self.repository = repository

    def get_sites(self) -> list[SiteDetail]:
        return self.repository.get_all()

    def get_site_by_code(self, code: str) -> SiteDetail | None:
        return self.repository.get_by_code(code=code)

    def create_site(self, site_create: SiteCreate) -> SiteDetail:
        return self.repository.create(entity_create=site_create.model_dump())

    def update_site(self, code: str, site_update: SiteUpdate) -> SiteDetail:
        return self.repository.update(
            code=code, entity_update=site_update.model_dump(exclude_unset=True)
        )

    def delete_site(self, code: str) -> None:
        self.repository.delete(code=code)
