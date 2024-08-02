from app.repository.role_repositpry import InMemoryRoleRepository
from app.roles.schemas import RoleDetail
from app.roles.service import RoleService


def test_get_roles(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    expected = role_repository.data[0]

    roles = service.get_roles()

    assert roles
    role = roles[0]
    assert isinstance(role, RoleDetail)
    assert hasattr(role, "id")
    assert role.code == expected.code
    assert role.description == expected.description


def test_get_role_by_code(role_repository: InMemoryRoleRepository) -> None:
    service = RoleService(repository=role_repository)
    expected = role_repository.data[0]

    role = service.get_role_by_code(code=expected.code)

    assert isinstance(role, RoleDetail)
    assert hasattr(role, "id")
    assert role.code == expected.code
    assert role.description == expected.description
