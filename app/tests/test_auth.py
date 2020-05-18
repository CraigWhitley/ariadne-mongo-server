from user.models import User
from mongoengine.context_managers import switch_db
from utils.auth import hash_password, check_password
from utils.db import register_test_db
import pytest



@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()


def test_can_authenticate_password():
    """Tests whether a users hashed password can be authenticated"""
    with switch_db(User, 'test'):
        User.drop_collection()
        User(
            email="hashpass@test.com",
            password=hash_password("S0meFunkyP455"),
            first_name="Craig",
            last_name="Johnson",
        ).save()
        result = User.objects(email="hashpass@test.com").first()

        assert check_password("S0meFunkyP455", result.password)
