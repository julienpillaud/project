from typing import Generic, TypeVar

AbstractRepositoryType = TypeVar("AbstractRepositoryType")


class BaseService(Generic[AbstractRepositoryType]):
    def __init__(self, repository: AbstractRepositoryType):
        self.repository = repository
