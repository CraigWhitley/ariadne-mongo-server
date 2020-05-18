from user.models import User
from mongoengine.context_managers import switch_db
from utils.auth import hash_password, check_password, encode_jwt, \
                                                        decode_jwt
from utils.db import register_test_db
import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()
    load_dotenv()


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


def test_can_decode_jwt():
    """Tests if JWT can be sucessfully decoded"""
    encoded = encode_jwt({'email': 'test@test.com'})

    decoded = decode_jwt(encoded)

    assert decoded["email"] == "test@test.com"
