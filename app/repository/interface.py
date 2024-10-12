import uuid
from typing import Protocol, TypeVar

from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate
from app.sites.schemas import SiteCreate, SiteDetail, SiteUpdate
from app.users.schemas import UserCreate, UserDetail, UserUpdate

SchemaType = TypeVar("SchemaType")
CreateType_contra = TypeVar("CreateType_contra", contravariant=True)
UpdateType_contra = TypeVar("UpdateType_contra", contravariant=True)


class AbstractRepository(Protocol[SchemaType, CreateType_contra, UpdateType_contra]):
    def get_all(self) -> list[SchemaType]: ...

    def get(self, entity_id: uuid.UUID) -> SchemaType | None: ...

    def create(self, entity_create: CreateType_contra) -> SchemaType: ...

    def update(
        self, entity_id: uuid.UUID, entity_update: UpdateType_contra
    ) -> SchemaType: ...

    def delete(self, entity_id: uuid.UUID) -> None: ...


class AbstractUserRepository(
    AbstractRepository[UserDetail, UserCreate, UserUpdate], Protocol
):
    def get_by_upn(self, upn: str) -> UserDetail | None: ...

    def add_site_to_user(
        self, user_id: uuid.UUID, site_id: uuid.UUID
    ) -> UserDetail: ...

    def delete_site_from_user(self, user_id: uuid.UUID, site_id: uuid.UUID) -> None: ...


class AbstractRoleRepository(
    AbstractRepository[RoleDetail, RoleCreate, RoleUpdate], Protocol
):
    def get_by_code(self, code: str) -> RoleDetail | None: ...


class AbstractSiteRepository(
    AbstractRepository[SiteDetail, SiteCreate, SiteUpdate], Protocol
):
    def get_by_code(self, code: str) -> SiteDetail | None: ...
