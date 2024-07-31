from app.users.models import UserSQLRepository
from app.users.schemas import UserDetail


def test_sqlalchemy_repo_get_all(user_sqlalchemy_repo: UserSQLRepository) -> None:
    users = user_sqlalchemy_repo.get_all()

    assert users
    user = users[0]
    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == "user1@mail.com"
    assert user.first_name == "user 1"
    assert user.last_name == ""


def test_sqlalchemy_repo_get(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_id = user_sqlalchemy_repo.get_all()[0].id

    user = user_sqlalchemy_repo.get(entity_id=user_id)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == "user1@mail.com"
    assert user.first_name == "user 1"
    assert user.last_name == ""


def test_sqlalchemy_repo_create(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_create = {"upn": "newuser@mail.com", "first_name": "new user", "last_name": ""}

    user = user_sqlalchemy_repo.create(entity_create=user_create)

    assert isinstance(user, UserDetail)
    assert hasattr(user, "id")
    assert user.upn == user_create["upn"]
    assert user.first_name == user_create["first_name"]
    assert user.last_name == user_create["last_name"]


def test_fake_repo_update(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_id = user_sqlalchemy_repo.get_all()[0].id
    first_name = "new_name"

    user = user_sqlalchemy_repo.update(
        entity_id=user_id, entity_update={"first_name": first_name}
    )

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.first_name == first_name


def test_fake_repo_delete(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_id = user_sqlalchemy_repo.get_all()[0].id

    user_sqlalchemy_repo.delete(entity_id=user_id)

    user = user_sqlalchemy_repo.get(entity_id=user_id)
    assert user is None
