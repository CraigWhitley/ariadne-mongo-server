from modules.core.user.models import User
from modules.core.auth.service import AuthService
import pytest
from uuid import uuid4
from faker import Faker
from modules.core.auth.repository import AuthRepository
from modules.core.user.repository import UserRepository
from modules.core.role.repository import RoleRepository
from modules.core.permission.repository import PermissionRepository
from .mock_models import mock_context
from .setup import register_test_db, register_test_injections, \
                   teardown, load_permissions, drop_all_collections

faker = Faker()

_user_repo = UserRepository()
_auth_repo = AuthRepository()
_role_repo = RoleRepository()
_perm_repo = PermissionRepository()

_auth_service = AuthService()


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()


def generate_user():
    user = User(
        id=str(uuid4()),
        email=faker.ascii_company_email(),
        password=_auth_service.hash_password(
                    faker.password(length=10,
                                   digits=True,
                                   upper_case=True,
                                   lower_case=True)))
    return user


def test_user_is_created():
    """Tests whether a user can be added to the database"""
    User.drop_collection()

    user = generate_user()
    user.save()

    result = User.objects(email=user.email).first()

    assert result.email == user.email


def test_can_find_user_by_email():
    """Tests whether a user can be retrived by email"""
    user = generate_user()
    user.save()

    result = _user_repo.find_user_by_email(user.email)

    assert result.email == user.email


def test_can_find_user_by_id():
    """Tests whether a user can retrieved by id"""
    user = generate_user()
    user.save()

    result = _user_repo.find_user_by_id(user.id)

    assert result.id == user.id


def test_can_retrieve_list_of_users():
    """Tests whether a list of all users can be queried"""
    user = generate_user()
    user.save()

    users = _user_repo.get_all_users()

    assert users.first() is not None


def test_register_user_returns_correct_users_email():
    """Tests the user registration returns user"""
    user = {}
    user["email"] = "correct@email.com"
    user["password"] = "C0rrectP455@"

    _auth_repo.register_user(user)

    result = User.objects(email="correct@email.com").first()

    assert result.email == "correct@email.com"


def test_can_update_users_active_status():
    user = generate_user().save()

    data = {}
    data["userId"] = user.id
    data["isActive"] = False

    user = _user_repo.update_users_active_status(data)

    assert user.is_active is False


def test_resolve_me():
    """
    Tests a user can be retrieved using the JWT token in the
    request header as Bearer <token>
    """
    user = generate_user()

    token = _auth_service.get_token(user.email)

    user.access_token = token

    user.save()

    headers = {
      "authorization": "Bearer " + user.access_token
    }

    request = mock_context(headers)

    resolved_user = _user_repo.me(request)

    assert user.email == resolved_user.email


def test_can_get_all_users_permissions():
    """Tests we can get all of a users permissions"""

    load_permissions()

    user = generate_user()

    saved_user = user.save()

    test_role = _role_repo.create_new_role("Test")

    permissions = _perm_repo.get_all_permissions()

    test_role.update(permissions=permissions)

    saved_user.roles.append(test_role)

    saved_user.save()

    users_permissions = _user_repo.get_users_permissions(saved_user.id)

    assert len(users_permissions["permissions"]) > 0


def test_can_update_users_email():
    user = User(
        id=str(uuid4()),
        email="update@test.com",
        password=_auth_service.hash_password("T35tpass")
    ).save()

    data = {}
    data["userId"] = user.id
    data["currentEmail"] = user.email
    data["newEmail"] = "updated@test.com"
    data["password"] = "T35tpass"

    saved_user = _user_repo.update_email(data)

    assert saved_user.email == data["newEmail"]


def test_can_add_whitelist_to_user():
    route = "test:route"

    data = _create_user_and_test_permission(route, "Whitelist test.")

    user = _user_repo.add_whitelist_to_user(data)

    result = any(x.route == route for x in user.whitelist)

    assert result is True


def test_can_add_blacklist_to_user():
    load_permissions()

    route = "test:blacklist_route"

    data = _create_user_and_test_permission(route, "Blacklist test.")

    user = _user_repo.add_blacklist_to_user(data)

    result = any(x.route == route for x in user.blacklist)

    assert result is True


def test_can_remove_blacklist_from_user():
    load_permissions()

    route = "test:remove_blacklist_route"

    data = _create_user_and_test_permission(route, "Test to remove blacklist.")

    _user_repo.add_blacklist_to_user(data)

    user = _user_repo.delete_blacklist_from_user(data)

    result = any(x.route == route for x in user.blacklist)

    assert result is False


def test_can_remove_whitelist_from_user():
    load_permissions()

    route = "test:remove_whitelist_route"

    data = _create_user_and_test_permission(route, "Test for whitelists.")

    _user_repo.add_whitelist_to_user(data)

    user = _user_repo.delete_whitelist_from_user(data)

    result = any(x.route == route for x in user.whitelist)

    assert result is False


def _create_user_and_test_permission(route="test:route",
                                     description="Just a test.") -> dict:
    """
    Helper function to generate a user and permission for the whitelist
    and blacklist tests.
    """
    user = generate_user().save()

    permission = _perm_repo.create_new_permission(route, description)

    data = {}
    data["userId"] = user.id
    data["permissionId"] = permission.id

    return data


def test_can_add_role_to_user():
    role = _role_repo.create_new_role("Testing Role")

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

    result = _user_repo.add_role_to_user(data)

    assert result is not None


def tests_teardown():
    drop_all_collections()
    teardown()
