from modules.core.user.models import User
from modules.core.auth.security import hash_password
from resolvers.user import resolve_find_user_by_email, \
                            resolve_all_users
from resolvers.auth import resolve_register_user
from utils.db import register_test_db
import pytest
from uuid import uuid4


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()


def test_user_is_created():
    """Tests whether a user can be added to the database"""
    User.drop_collection()
    User(
        id=str(uuid4()),
        email="isthisintest@test.com",
        password=hash_password("Somethingover8"),
        first_name="Joe",
        last_name="Johnson",
    ).save()
    result = User.objects(email="isthisintest@test.com").first()

    assert result.email == "isthisintest@test.com"


def test_can_find_user_by_email():
    """Tests whether a user can be queried by email"""
    user = resolve_find_user_by_email(None, None, "isthisintest@test.com")

    assert user.email == "isthisintest@test.com"


def test_can_retrieve_list_of_users():
    """Tests whether a list of all users can be queried"""
    users = resolve_all_users(None, None)

    assert users.first() is not None


def test_register_user_resolver_returns_token_on_valid_user():
    """Tests the user registration resolver returns token"""
    User.drop_collection()
    user = {}
    user["email"] = "correct@email.com"
    user["password"] = "C0rrectP455@"
    user["firstName"] = "Jenny"
    user["lastName"] = "Sandsworth"

    resolve_register_user(None, None, user)

    result = User.objects(email="correct@email.com").first()

    assert result.email == "correct@email.com"
