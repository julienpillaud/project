from app.users.schemas import UserCreate, UserDetail, UserUpdate
from app.users.service import UserService
from tests.conftest import UserInMemoryRepository


def test_get_users(user_inmemory_repo: UserInMemoryRepository) -> None:
    assert UserService.get_users(repository=user_inmemory_repo) == [
        UserDetail(id=1, email="user1@mail.com", username="user 1"),
        UserDetail(id=2, email="user2@mail.com", username="user 2"),
    ]


def test_get_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = 1

    assert UserService.get_user(
        repository=user_inmemory_repo, user_id=user_id
    ) == UserDetail(id=1, email="user1@mail.com", username="user 1")


def test_create_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_create = UserCreate(email="newuser@mail.com", username="new user")

    user = UserService.create_user(
        repository=user_inmemory_repo, user_create=user_create
    )

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.email == user_create.email
    assert user.username == user_create.username


def test_update_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = 1
    user_update = UserUpdate(username="new username")

    user = UserService.update_user(
        repository=user_inmemory_repo, user_id=user_id, user_update=user_update
    )

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.username == user_update.username


def test_delete_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = 1

    UserService.delete_user(repository=user_inmemory_repo, user_id=user_id)

    user = user_inmemory_repo.get(entity_id=user_id)
    assert user is None
