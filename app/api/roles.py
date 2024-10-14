import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.services import ServiceDependencyFactory
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate
from app.roles.service import RoleService

router = APIRouter(tags=["roles"], prefix="/roles")

role_service_dependency_factory = ServiceDependencyFactory(service_name="role")
RoleServiceDependency = Annotated[
    RoleService, Depends(role_service_dependency_factory.dependency())
]


@router.get("/", response_model=list[RoleDetail])
def get_roles(role_service: RoleServiceDependency) -> Any:
    return role_service.get_roles()


@router.get("/{role_id}", response_model=RoleDetail)
def get_role(role_id: uuid.UUID, role_service: RoleServiceDependency) -> Any:
    if role := role_service.get_role(role_id=role_id):
        return role
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


@router.post("/", response_model=RoleDetail)
def create_role(role_service: RoleServiceDependency, role_create: RoleCreate) -> Any:
    if role_service.get_role_by_code(code=role_create.code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role already exists"
        )
    return role_service.create_role(role_create=role_create)


@router.patch("/{role_id}", response_model=RoleDetail)
def update_role(
    role_service: RoleServiceDependency, role_id: uuid.UUID, role_update: RoleUpdate
) -> Any:
    if not role_service.get_role(role_id=role_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role_service.update_role(role_id=role_id, role_update=role_update)


@router.delete("/{role_id}")
def delete_role(role_service: RoleServiceDependency, role_id: uuid.UUID) -> None:
    if not role_service.get_role(role_id=role_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    role_service.delete_role(role_id=role_id)
