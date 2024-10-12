from app.repository.inmemory.user import InMemoryUserRepository
from app.users.schemas import UserCreate, UserDetail
from app.users.service import UserService


def test_get_users(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)

    users = service.get_users()

    assert len(users) == len(user_repository.data)


def test_get_user(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    expected = user_repository.data[0]

    user = service.get_user(user_id=expected.id)

    assert isinstance(user, UserDetail)
    assert user.upn == expected.upn
    assert user.first_name == expected.first_name
    assert user.last_name == expected.last_name


def test_get_user_by_upn(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    expected = user_repository.data[0]

    user = service.get_user_by_upn(upn=expected.upn)

    assert isinstance(user, UserDetail)
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
    assert user.upn == user_create.upn
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


def test_delete_user(user_repository: InMemoryUserRepository) -> None:
    service = UserService(repository=user_repository)
    nb_users = len(user_repository.data)
    user_id = user_repository.data[0].id

    service.delete_user(user_id=user_id)

    assert len(user_repository.data) == nb_users - 1
