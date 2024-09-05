from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_site_service
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate
from app.sites.service import SiteService

router = APIRouter(tags=["sites"], prefix="/sites")


SiteServiceDependency = Annotated[SiteService, Depends(get_site_service)]


@router.get("/", response_model=list[SiteDetail])
def get_sites(site_service: SiteServiceDependency) -> Any:
    return site_service.get_sites()


@router.get("/{code}", response_model=SiteDetail)
def get_site(code: str, site_service: SiteServiceDependency) -> Any:
    if site := site_service.get_site_by_code(code=code):
        return site
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")


@router.post("/", response_model=SiteDetail)
def create_site(site_service: SiteServiceDependency, site_create: SiteCreate) -> Any:
    if site_service.get_site_by_code(code=site_create.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Site already exists"
        )
    return site_service.create_site(site_create=site_create)


@router.patch("/{code}", response_model=SiteDetail)
def update_site(
    site_service: SiteServiceDependency, code: str, site_update: SiteUpdate
) -> Any:
    if not site_service.get_site_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    return site_service.update_site(code=code, site_update=site_update)


@router.delete("/{code}")
def delete_site(site_service: SiteServiceDependency, code: str) -> None:
    if not site_service.get_site_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    site_service.delete_site(code=code)
