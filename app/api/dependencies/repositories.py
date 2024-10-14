import importlib
import logging
from collections.abc import Callable
from typing import Annotated

from fastapi import Depends

from app.entities import DatabaseType, ServiceName

logger = logging.getLogger(__name__)


class BaseRepositoryDependency:
    def __init__(self, service_name: ServiceName) -> None:
        self.service_name = service_name


repositories_map: dict[DatabaseType, str] = {
    DatabaseType.INMEMORY: "InMemoryRepositoryDependency",
    DatabaseType.SQLALCHEMY: "SQLAlchemyRepositoryDependency",
}


def get_repository_class(
    database_type: DatabaseType,
) -> type[BaseRepositoryDependency]:
    module = importlib.import_module(f"app.api.dependencies.{database_type}")
    class_name = repositories_map[database_type]
    return getattr(module, class_name)  # type: ignore


class RepositoryDependencyFactory:
    def __init__(self, database_type: DatabaseType, service_name: ServiceName) -> None:
        repository_class = get_repository_class(database_type=database_type)
        self.repository_dependency = repository_class(service_name=service_name)

    def dependency(
        self,
    ) -> Callable[[BaseRepositoryDependency], BaseRepositoryDependency]:
        repository_dependency = self.repository_dependency

        def _dependency(
            repository: Annotated[
                BaseRepositoryDependency, Depends(repository_dependency)
            ],
        ) -> BaseRepositoryDependency:
            return repository

        return _dependency
