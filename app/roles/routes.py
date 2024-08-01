import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_session
from app.repository.interface import AbstractRepository
from app.roles.models import RoleSQLRepository
from app.roles.schemas import RoleDetail
from app.roles.service import RoleService

router = APIRouter(tags=["roles"], prefix="/roles")


def get_repository(
    session: Annotated[Session, Depends(get_session)],
) -> RoleSQLRepository:
    return RoleSQLRepository(session=session)


RepositoryDependency = Annotated[
    AbstractRepository[RoleDetail], Depends(get_repository)
]


@router.get("/", response_model=list[RoleDetail])
def get_roles(repository: RepositoryDependency) -> Any:
    return RoleService.get_roles(repository=repository)


@router.get("/{role_id}", response_model=RoleDetail)
def get_role(repository: RepositoryDependency, role_id: uuid.UUID) -> Any:
    role = RoleService.get_role(repository=repository, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
