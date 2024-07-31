from app.users.schemas import UserCreate, UserDetail, UserUpdate
from app.users.service import UserService
from tests.conftest import UserInMemoryRepository


def test_get_users(user_inmemory_repo: UserInMemoryRepository) -> None:
    users = UserService.get_users(repository=user_inmemory_repo)

    assert users
    user = users[0]
    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == "user1@mail.com"
    assert user.first_name == "user 1"
    assert user.last_name == ""


def test_get_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = user_inmemory_repo.fake_data[0].id

    user = UserService.get_user(repository=user_inmemory_repo, user_id=user_id)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == "user1@mail.com"
    assert user.first_name == "user 1"
    assert user.last_name == ""


def test_create_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_create = UserCreate(
        upn="newuser@mail.com", first_name="new user", last_name=""
    )

    user = UserService.create_user(
        repository=user_inmemory_repo, user_create=user_create
    )

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == user_create.upn
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


def test_update_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = user_inmemory_repo.fake_data[0].id
    user_update = UserUpdate(first_name="new username")

    user = UserService.update_user(
        repository=user_inmemory_repo, user_id=user_id, user_update=user_update
    )

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.first_name == user_update.first_name


def test_delete_user(user_inmemory_repo: UserInMemoryRepository) -> None:
    user_id = user_inmemory_repo.fake_data[0].id

    UserService.delete_user(repository=user_inmemory_repo, user_id=user_id)

    user = user_inmemory_repo.get(entity_id=user_id)
    assert user is None
