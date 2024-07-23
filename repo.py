from collections.abc import Iterator
from typing import Any, Generic, Protocol, Type, TypeVar

import pytest
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declared_attr,
    mapped_column,
)


class GenericBaseModel(BaseModel):
    id: int


class UserDetail(GenericBaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


# ------------------------------------------------------------------------------
EntityType = TypeVar("EntityType", bound=GenericBaseModel)


class AbstractRepository(Protocol[EntityType]):
    """AbstractRepository inherits from Protocol to have abstract methods."""

    entity: Type[EntityType]

    def get_all(self) -> list[EntityType]: ...

    def get(self, entity_id: int) -> EntityType | None: ...

    def create(self, entity_create: dict[str, Any]) -> EntityType: ...

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None: ...


# ------------------------------------------------------------------------------
# SQLAlchemy abstract
# https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base
class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


ModelType = TypeVar("ModelType", bound=Base)


class AbstractSQLAlchemyRepository(
    Generic[ModelType, EntityType],
    AbstractRepository[EntityType],
):
    """AbstractSQLAlchemyRepository inherits from AbstractRepository,
    so it's also a Protocol.
    Define a new generic type: ModelType (need to list all generic types here).
    """

    model: Type[ModelType]
    session: Session

    def get_all(self) -> list[EntityType]:
        stmt = select(self.model)
        entities = self.session.scalars(stmt)
        return [self.entity.model_validate(entity) for entity in entities]

    def get(self, entity_id: int) -> EntityType | None:
        # Need to have Base(DeclarativeBase) to call self.model.id
        stmt = select(self.model).where(self.model.id == entity_id)
        model_obj = self.session.scalars(stmt).first()
        return self.entity.model_validate(model_obj) if model_obj else None

    def create(self, entity_create: dict[str, Any]) -> EntityType:
        model_obj = self.model(**entity_create)
        self.session.add(model_obj)
        self.session.commit()
        return self.entity.model_validate(model_obj)

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None:
        stmt = select(self.model).where(self.model.id == entity_id)
        model_obj = self.session.scalars(stmt).first()
        if not model_obj:
            return None

        for key, value in entity_update.items():
            if hasattr(model_obj, key):
                setattr(model_obj, key, value)
        self.session.commit()
        return self.entity.model_validate(model_obj)


# ------------------------------------------------------------------------------
# SQlAlchemy concrete
class User(Base):
    name: Mapped[str] = mapped_column(String(128))


class UserSQLRepository(AbstractSQLAlchemyRepository[User, UserDetail]):
    """Implement an SQLAlchemy repository with a User model."""

    def __init__(self, session: Session) -> None:
        self.entity = UserDetail
        self.session = session
        self.model = User


# ------------------------------------------------------------------------------
# Fake abstract
class AbstractFakeRepository(AbstractRepository[EntityType]):
    fake_data: list[EntityType]
    id_counter: int = 1

    def get_all(self) -> list[EntityType]:
        return [self.entity.model_validate(entity) for entity in self.fake_data]

    def get(self, entity_id: int) -> EntityType | None:
        # Need to have GenericBaseModel(BaseModel) to call entity.id
        return next(entity for entity in self.fake_data if entity.id == entity_id)

    def create(self, entity_create: dict[str, Any]) -> EntityType:
        entity_create["id"] = self.id_counter
        data = self.entity.model_validate(entity_create)
        self.fake_data.append(data)
        self.id_counter += 1
        return data

    def update(
        self, entity_id: int, entity_update: dict[str, Any]
    ) -> EntityType | None:
        entity = next(entity for entity in self.fake_data if entity.id == entity_id)
        if not entity:
            return None

        for key, value in entity_update.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        return entity


# ------------------------------------------------------------------------------
# Fake concrete
class UserFakeRepository(AbstractFakeRepository[UserDetail]):
    """Implement a fake repository with UserDetail schema."""

    def __init__(self, input_data: list[dict[str, Any]]) -> None:
        self.entity = UserDetail
        self.fake_data = [self.entity.model_validate(data) for data in input_data]


# ------------------------------------------------------------------------------
# Tests
@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as sql_session:
        user_1 = User(id=1, name="user 1")
        user_2 = User(id=2, name="user 2")
        sql_session.add(user_1)
        sql_session.add(user_2)
        sql_session.commit()
        yield sql_session


@pytest.fixture()
def user_sql_repo(session: Session) -> UserSQLRepository:
    return UserSQLRepository(session=session)


@pytest.fixture()
def user_fake_repo(session: Session) -> UserFakeRepository:
    data_from_yaml: list[dict[str, Any]] = [
        {"id": 1, "name": "user 1"},
        {"id": 2, "name": "user 2"},
    ]
    return UserFakeRepository(input_data=data_from_yaml)


def test_sql_repository_get_all(user_sql_repo: UserSQLRepository) -> None:
    assert user_sql_repo.get_all() == [
        UserDetail(id=1, name="user 1"),
        UserDetail(id=2, name="user 2"),
    ]


def test_sql_repository_get(user_sql_repo: UserSQLRepository) -> None:
    assert user_sql_repo.get(entity_id=1) == UserDetail(id=1, name="user 1")


def test_sql_repo_create(user_sql_repo: UserSQLRepository) -> None:
    name = "new_user"
    new_user = user_sql_repo.create(entity_create={"name": name})
    assert isinstance(new_user, UserDetail)
    assert hasattr(new_user, "id")
    assert new_user.name == name


def test_fake_repo_get_all(user_fake_repo: UserFakeRepository) -> None:
    assert user_fake_repo.get_all() == [
        UserDetail(id=1, name="user 1"),
        UserDetail(id=2, name="user 2"),
    ]


def test_fake_repo_get(user_fake_repo: UserFakeRepository) -> None:
    assert user_fake_repo.get(entity_id=1) == UserDetail(id=1, name="user 1")


def test_fake_repo_create(user_fake_repo: UserFakeRepository) -> None:
    name = "new_user"
    new_user = user_fake_repo.create(entity_create={"name": name})
    assert isinstance(new_user, UserDetail)
    assert hasattr(new_user, "id")
    assert new_user.name == name


if __name__ == "__main__":
    pytest.main()
