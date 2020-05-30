from modules.core.permission.models import Permission
from modules.core.auth.service import AuthService
import pytest
from uuid import uuid4
from faker import Faker
from modules.core.role.models import Role
from modules.core.auth.repository import AuthRepository
from modules.core.permission.repository import PermissionRepository
from modules.core.role.repository import RoleRepository
from .setup import register_test_db, register_test_injections, \
                   teardown, load_permissions, drop_all_collections

faker = Faker()

_auth_repo = AuthRepository()
_role_repo = RoleRepository()
_perm_repo = PermissionRepository()

_auth_service = AuthService()


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()
    load_permissions()


def generate_roles(amount=5):
    roles = []

    for _ in range(amount):
        roles.append(
            Role(
             id=str(uuid4()),
             name=faker.word()
            )
        )

    return roles


def generate_role():
    role = Role(
              id=str(uuid4()),
              name=faker.word()
            )

    return role


def test_can_get_a_list_of_all_roles():
    roles = generate_roles(amount=10)
    for role in roles:
        role.save()

    result = _role_repo.get_all_roles()

    assert len(result) > 0


def test_can_find_a_role_by_its_id():
    role = generate_role().save()

    result = _role_repo.find_role_by_id(role.id)

    assert result is not None


def test_can_add_permission_to_role():
    permission = Permission(
        id=str(uuid4()),
        route="test:test_route",
        description="Test description"
    ).save()

    role = Role(
        id=str(uuid4()),
        name="Test"
    ).save()

    data = {}
    data["permissionId"] = permission.id
    data["roleId"] = role.id

    role: Role = _role_repo.add_permission_to_role(data)

    assert role is not None


def test_we_can_add_a_new_role():
    role = _role_repo.create_new_role("Testing")

    result = Role.objects(name=role.name).first()

    assert result is not None


def tests_teardown():
    drop_all_collections()
    teardown()
