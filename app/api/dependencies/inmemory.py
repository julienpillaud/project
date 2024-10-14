from typing import Any

from app.api.dependencies.repositories import BaseRepositoryDependency
from app.entities import ServiceName
from app.repository.inmemory.role import InMemoryRoleRepository
from app.repository.inmemory.site import InMemorySiteRepository
from app.repository.inmemory.user import InMemoryUserRepository

repositories_map: dict[ServiceName, type[Any]] = {
    "role": InMemoryRoleRepository,
    "site": InMemorySiteRepository,
    "user": InMemoryUserRepository,
}


class InMemoryRepositoryDependency(BaseRepositoryDependency):
    def __init__(self, service_name: ServiceName) -> None:
        super().__init__(service_name)
        self.repository = repositories_map[service_name](data=[])

    def __call__(self) -> Any:
        return self.repository
