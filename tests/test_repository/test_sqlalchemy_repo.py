from app.users.models import UserSQLRepository
from app.users.schemas import UserDetail


def test_sqlalchemy_repo_get_all(user_sqlalchemy_repo: UserSQLRepository) -> None:
    assert user_sqlalchemy_repo.get_all() == [
        UserDetail(id=1, name="user 1"),
        UserDetail(id=2, name="user 2"),
    ]


def test_sqlalchemy_repo_get(user_sqlalchemy_repo: UserSQLRepository) -> None:
    assert user_sqlalchemy_repo.get(entity_id=1) == UserDetail(id=1, name="user 1")


def test_sqlalchemy_repo_create(user_sqlalchemy_repo: UserSQLRepository) -> None:
    name = "new_user"

    new_user = user_sqlalchemy_repo.create(entity_create={"name": name})

    assert isinstance(new_user, UserDetail)
    assert hasattr(new_user, "id")
    assert new_user.name == name


def test_fake_repo_update(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_id = 1
    name = "new_user"

    user = user_sqlalchemy_repo.update(entity_id=user_id, entity_update={"name": name})

    assert isinstance(user, UserDetail)
    assert user.id == user_id
    assert user.name == name


def test_fake_repo_delete(user_sqlalchemy_repo: UserSQLRepository) -> None:
    user_sqlalchemy_repo.delete(entity_id=1)

    user = user_sqlalchemy_repo.get(entity_id=1)
    assert user is None
