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
    role_code = role_repository.data[0].code
    role_update = RoleUpdate(description="role updated")

    role = service.update_role(code=role_code, role_update=role_update)

    assert isinstance(role, RoleDetail)
    assert role.code == role_code
    assert role.description == role_update.description


def test_delete_role(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    nb_roles = len(role_repository.data)
    role_code = role_repository.data[0].code

    service.delete_role(code=role_code)

    assert len(role_repository.data) == nb_roles - 1
