from modules.core.user.models import User
from modules.core.permission.models import Permission
from modules.core.auth.service import AuthService
import pytest
from uuid import uuid4
from faker import Faker
from modules.core.role.models import Role
from modules.core.auth.repository import AuthRepository
from modules.core.role.repository import RoleRepository
from .setup import register_test_db, register_test_injections, \
                   teardown, load_permissions, drop_all_collections

faker = Faker()

_auth_repo = AuthRepository()
_role_repo = RoleRepository()

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


def test_can_get_a_list_of_all_permissions():
    permissions = _role_repo.get_all_permissions()

    assert len(permissions) > 0


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


def test_can_add_role_to_user():
    role = generate_role().save()
    user = User(
        id=str(uuid4()),
        email=faker.ascii_company_email(),
        password=_auth_service.hash_password(
                    faker.password(length=10,
                                   digits=True,
                                   upper_case=True,
                                   lower_case=True)))

    user.save()

    data = {}
    data["roleId"] = role.id
    data["userId"] = user.id

    result = _role_repo.add_role_to_user(data)

    assert result is not None


def test_we_can_add_a_new_role():
    role = _role_repo.create_new_role("Testing")

    result = Role.objects(name=role.name).first()

    assert result is not None


def test_can_create_new_permission():
    permission = _role_repo.create_new_permission(
                    route="test:test_new_perm",
                    description="Just a test permissions.")

    result = Permission.objects(route=permission.route).first()

    assert result is not None


def tests_teardown():
    drop_all_collections()
    teardown()
