from user.models import User
from mongoengine.context_managers import switch_db
from utils.auth import hash_password
from resolvers.user import resolve_find_user_by_email, \
                            resolve_all_users
from utils.db import register_test_db
import pytest


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()


def test_user_is_created():
    """Tests whether a user can be added to the database"""
    with switch_db(User, 'test'):
        User.drop_collection()
        User(
            email="test@test.com",
            password=hash_password("somethingover8"),
            first_name="Joe",
            last_name="Johnson",
        ).save()
        result = User.objects(email="test@test.com").first()

        assert result.email == "test@test.com"


def test_can_find_user_by_email():
    """Tests whether a user can be queried by email"""
    user = resolve_find_user_by_email(None, None, "test@test.com")

    assert user.email == "test@test.com"


def test_can_retrieve_list_of_users():
    """Test whether a list of all users can be queried"""
    users = resolve_all_users(None)

    assert users.first() is not None
