import os
from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends

from app.api.dependencies.repositories import (
    BaseRepositoryDependency,
    RepositoryDependencyFactory,
)
from app.entities import DatabaseType, ServiceName
from app.roles.service import RoleService
from app.sites.service import SiteService
from app.users.service import UserService

services_map = {
    "role": RoleService,
    "site": SiteService,
    "user": UserService,
}


class ServiceDependencyFactory:
    def __init__(self, service_name: ServiceName) -> None:
        self.service_name = service_name
        self.service = services_map[self.service_name]
        database_type = os.getenv("DATABASE_TYPE", DatabaseType.INMEMORY)
        self.database_type = DatabaseType(database_type)
        self.repository_dependency_factory = RepositoryDependencyFactory(
            database_type=self.database_type, service_name=self.service_name
        )

    def dependency(
        self,
    ) -> Callable[
        [Callable[[BaseRepositoryDependency], BaseRepositoryDependency]], Any
    ]:
        repository_dependency_factory = self.repository_dependency_factory

        def _dependency(
            repository: Annotated[
                Callable[[BaseRepositoryDependency], BaseRepositoryDependency],
                Depends(repository_dependency_factory.dependency()),
            ],
        ) -> Any:
            return self.service(repository=repository)

        return _dependency
