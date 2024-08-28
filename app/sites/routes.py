from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.site_repositpry import SQLAlchemySiteRepository
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate
from app.sites.service import SiteService

router = APIRouter(tags=["sites"], prefix="/sites")


def get_service(session: Annotated[Session, Depends(get_session)]) -> SiteService:
    repository = SQLAlchemySiteRepository(session=session)
    return SiteService(repository=repository)


ServiceDependency = Annotated[SiteService, Depends(get_service)]


@router.get("/", response_model=list[SiteDetail])
def get_sites(service: ServiceDependency) -> Any:
    return service.get_sites()


@router.get("/{code}", response_model=SiteDetail)
def get_site(code: str, service: ServiceDependency) -> Any:
    if site := service.get_site_by_code(code=code):
        return site
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")


@router.post("/", response_model=SiteDetail)
def create_site(service: ServiceDependency, site_create: SiteCreate) -> Any:
    if service.get_site_by_code(code=site_create.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Site already exists"
        )
    return service.create_site(site_create=site_create)


@router.patch("/{code}", response_model=SiteDetail)
def update_site(service: ServiceDependency, code: str, site_update: SiteUpdate) -> Any:
    if not service.get_site_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    return service.update_site(code=code, site_update=site_update)


@router.delete("/{code}")
def delete_site(service: ServiceDependency, code: str) -> None:
    if not service.get_site_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    service.delete_site(code=code)
