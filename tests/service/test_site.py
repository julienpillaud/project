from app.repository.site_repository import InMemorySiteRepository
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate
from app.sites.service import SiteService


def test_get_sites(site_repository: InMemorySiteRepository) -> None:
    service = SiteService(repository=site_repository)

    sites = service.get_sites()

    assert len(sites) == len(site_repository.data)


def test_create_site(site_repository: InMemorySiteRepository) -> None:
    service = SiteService(repository=site_repository)
    site_create = SiteCreate(code="NEW", name="new site")

    site = service.create_site(site_create=site_create)

    assert isinstance(site, SiteDetail)
    assert site.code == site_create.code
    assert site.name == site_create.name


def test_update_site(site_repository: InMemorySiteRepository) -> None:
    service = SiteService(repository=site_repository)
    site_db = site_repository.data[0]
    site_update = SiteUpdate(name="site updated")

    site = service.update_site(site_id=site_db.id, site_update=site_update)

    assert isinstance(site, SiteDetail)
    assert site.id == site_db.id
    assert site.code == site_db.code
    assert site.name == site_update.name


def test_delete_site(site_repository: InMemorySiteRepository) -> None:
    service = SiteService(repository=site_repository)
    nb_sites = len(site_repository.data)
    site_db = site_repository.data[0]

    service.delete_site(site_id=site_db.id)

    assert len(site_repository.data) == nb_sites - 1
