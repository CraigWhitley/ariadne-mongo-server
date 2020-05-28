from modules.core.user.models import User
from modules.core.auth.service import AuthService
import pytest
from uuid import uuid4
from faker import Faker
from modules.core.auth.repository import AuthRepository
from modules.core.user.repository import UserRepository
from modules.core.role.repository import RoleRepository
from .mock_models import mock_context
from .setup import register_test_db, register_test_injections, \
                   teardown, load_permissions, drop_all_collections

faker = Faker()

_user_repo = UserRepository()
_auth_repo = AuthRepository()
_role_repo = RoleRepository()

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
    """Tests whether a user can be queried by email"""
    user = generate_user()
    user.save()

    result = _user_repo.find_user_by_email(user.email)

    assert result.email == user.email


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

    permissions = _role_repo.get_all_permissions()

    test_role.update(permissions=permissions)

    saved_user.roles.append(test_role)

    saved_user.save()

    users_permissions = _user_repo.get_users_permissions(saved_user.email)

    assert len(users_permissions["permissions"]) > 0


def test_can_update_users_email():
    User(
        id=str(uuid4()),
        email="update@test.com",
        password=_auth_service.hash_password("T35tpass")
    ).save()

    data = {}
    data["currentEmail"] = "update@test.com"
    data["newEmail"] = "updated@test.com"
    data["password"] = "T35tpass"

    user = _user_repo.update_email(data)

    assert user.email == data["newEmail"]


def tests_teardown():
    drop_all_collections()
    teardown()
