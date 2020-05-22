from modules.core.user.models import User
from modules.core.auth.security import hash_password, \
                                        encode_jwt
from utils.db import register_test_db
import pytest
from uuid import uuid4
from faker import Faker
from modules.core.auth.models import JwtPayload
from modules.core.auth.repository import register_user
from modules.core.user.repository import fetch_all_users, \
                                        find_user_by_email, me
from .mock_models import mock_context
from graphql import GraphQLResolveInfo

faker = Faker()


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()


def generate_user():
    user = User(
        id=str(uuid4()),
        email=faker.ascii_company_email(),
        password=hash_password(
                    faker.password(length=10,
                                   digits=True,
                                   upper_case=True,
                                   lower_case=True)),
        first_name=faker.first_name(),
        last_name=faker.last_name())
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

    result = find_user_by_email(user.email)

    assert result.email == user.email


def test_can_retrieve_list_of_users():
    """Tests whether a list of all users can be queried"""
    user = generate_user()
    user.save()
    users = fetch_all_users()

    assert users.first() is not None


def test_register_user_returns_correct_users_email():
    """Tests the user registration returns user"""
    user = {}
    user["email"] = "correct@email.com"
    user["password"] = "C0rrectP455@"
    user["firstName"] = "Jenny"
    user["lastName"] = "Sandsworth"

    register_user(user)

    result = User.objects(email="correct@email.com").first()

    assert result.email == "correct@email.com"


def test_resolve_me():
    """
    Tests a user can be retrieved using the JWT token in the
    request header as Bearer <token>
    """
    user = generate_user()

    jwt_payload = JwtPayload(user.email)

    token = encode_jwt(jwt_payload.get())

    user.access_token = str(token, 'utf8')
    user.save()

    headers = {
      "authorization": "Bearer " + user.access_token
    }

    request = mock_context(headers)

    resolved_user = me(request)

    assert user.email == resolved_user.email
