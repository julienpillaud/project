from app.users.schemas import UserDetail
from tests.conftest import UserInMemoryRepository


def test_inmemory_repo_get_all(user_inmemory_repo: UserInMemoryRepository) -> None:
    assert user_inmemory_repo.get_all() == [
        UserDetail(id=1, email="user1@mail.com", username="user 1"),
        UserDetail(id=2, email="user2@mail.com", username="user 2"),
    ]


def test_fake_repo_get(user_inmemory_repo: UserInMemoryRepository) -> None:
    assert user_inmemory_repo.get(entity_id=1) == UserDetail(
        id=1, email="user1@mail.com", username="user 1"
    )


def test_fake_repo_create(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_create = {"email": "newuser@mail.com", "username": "new user"}

    user = user_inmemory_repo.create(entity_create=user_create)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.email == user_create["email"]
    assert user.username == user_create["username"]


def test_fake_repo_update(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = 1
    username = "new_name"

    user = user_inmemory_repo.update(
        entity_id=user_id, entity_update={"username": username}
    )

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.username == username


def test_fake_repo_delete(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_inmemory_repo.delete(entity_id=1)

    user = user_inmemory_repo.get(entity_id=1)
    assert user is None
