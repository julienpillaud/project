from app.repository.role_repositpry import InMemoryRoleRepository
from app.roles.schemas import RoleCreate, RoleDetail, RoleUpdate
from app.roles.service import RoleService


def test_get_roles(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)

    roles = service.get_roles()

    assert len(roles) == len(role_repository.data)


def test_get_role_by_code(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    expected = role_repository.data[0]

    role = service.get_role_by_code(code=expected.code)

    assert isinstance(role, RoleDetail)
    assert role.code == expected.code
    assert role.description == expected.description


def test_create_role(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    role_create = RoleCreate(code="NEW ROLE", description="new role")

    role = service.create_role(role_create=role_create)

    assert isinstance(role, RoleDetail)
    assert role.code == role_create.code
    assert role.description == role_create.description


def test_update_role(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    role_db = role_repository.data[0]
    role_update = RoleUpdate(description="role updated")

    role = service.update_role(role_id=role_db.id, role_update=role_update)

    assert isinstance(role, RoleDetail)
    assert role.id == role_db.id
    assert role.code == role_db.code
    assert role.description == role_update.description


def test_delete_role(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    nb_roles = len(role_repository.data)
    role_db = role_repository.data[0]

    service.delete_role(role_id=role_db.id)

    assert len(role_repository.data) == nb_roles - 1
