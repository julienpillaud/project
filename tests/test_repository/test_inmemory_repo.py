from app.users.schemas import UserDetail
from tests.test_repository.conftest import UserInMemoryRepository


def test_inmemory_repo_get_all(user_inmemory_repo: UserInMemoryRepository) -> None:
    assert user_inmemory_repo.get_all() == [
        UserDetail(id=1, name="user 1"),
        UserDetail(id=2, name="user 2"),
    ]


def test_fake_repo_get(user_inmemory_repo: UserInMemoryRepository) -> None:
    assert user_inmemory_repo.get(entity_id=1) == UserDetail(id=1, name="user 1")


def test_fake_repo_create(user_inmemory_repo: UserInMemoryRepository) -> None:
    name = "new_user"

    user = user_inmemory_repo.create(entity_create={"name": name})

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.name == name


def test_fake_repo_update(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = 1
    name = "new_user"

    user = user_inmemory_repo.update(entity_id=user_id, entity_update={"name": name})

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.name == name


def test_fake_repo_delete(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_inmemory_repo.delete(entity_id=1)

    user = user_inmemory_repo.get(entity_id=1)
    assert user is None
