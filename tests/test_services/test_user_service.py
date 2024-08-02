from app.repository.user_repository import InMemoryUserRepository
from app.users.schemas import UserCreate, UserDetail
from app.users.service import UserService


def test_get_users(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    expected = user_repository.data[0]

    users = service.get_users()

    assert users
    user = users[0]
    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == expected.upn
    assert user.first_name == expected.first_name
    assert user.last_name == expected.last_name


def test_get_user(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    expected = user_repository.data[0]
    user_id = user_repository.data[0].id

    user = service.get_user(user_id=user_id)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == expected.upn
    assert user.first_name == expected.first_name
    assert user.last_name == expected.last_name


def test_create_user(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    user_create = UserCreate(
        upn="newuser@mail.com", first_name="new user", last_name=""
    )

    user = service.create_user(user_create=user_create)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == user_create.upn
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name
