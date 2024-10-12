from app.repository.inmemory.base import InMemoryRepositoryBase
from app.repository.interface import AbstractSiteRepository
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate


class InMemorySiteRepository(
    AbstractSiteRepository, InMemoryRepositoryBase[SiteDetail, SiteCreate, SiteUpdate]
):
    model = SiteDetail

    def get_by_code(self, code: str) -> SiteDetail | None:
        return next((entity for entity in self.data if entity.code == code), None)
