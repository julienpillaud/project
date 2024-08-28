from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.role_repositpry import SQLAlchemyRoleRepository
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate
from app.roles.service import RoleService

router = APIRouter(tags=["roles"], prefix="/roles")


def get_service(session: Annotated[Session, Depends(get_session)]) -> RoleService:
    repository = SQLAlchemyRoleRepository(session=session)
    return RoleService(repository=repository)


ServiceDependency = Annotated[RoleService, Depends(get_service)]


@router.get("/", response_model=list[RoleDetail])
def get_roles(service: ServiceDependency) -> Any:
    return service.get_roles()


@router.get("/{code}", response_model=RoleDetail)
def get_role(code: str, service: ServiceDependency) -> Any:
    if role := service.get_role_by_code(code=code):
        return role
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@router.post("/", response_model=RoleDetail)
def create_role(service: ServiceDependency, role_create: RoleCreate) -> Any:
    if service.get_role_by_code(code=role_create.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role already exists"
        )
    return service.create_role(role_create=role_create)


@router.patch("/{code}", response_model=RoleDetail)
def update_role(service: ServiceDependency, code: str, role_update: RoleUpdate) -> Any:
    if not service.get_role_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return service.update_role(code=code, role_update=role_update)


@router.delete("/{code}")
def delete_role(service: ServiceDependency, code: str) -> None:
    if not service.get_role_by_code(code=code):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    service.delete_role(code=code)
