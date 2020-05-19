from user.models import User
from utils.auth import hash_password, check_password, encode_jwt, \
                                                        decode_jwt
from utils.db import register_test_db
import pytest
from dotenv import load_dotenv
from auth.models import JwtPayload


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()
    load_dotenv()


@pytest.fixture
def encoded_jwt():
    payload = JwtPayload('test@test.com')

    encoded = encode_jwt(payload.get())

    return encoded


def test_can_authenticate_password():
    """Tests whether a users hashed password can be authenticated"""
    User.drop_collection()
    User(
        email="hashpass@test.com",
        password=hash_password("S0meFunkyP455"),
        first_name="Craig",
        last_name="Johnson",
    ).save()
    result = User.objects(email="hashpass@test.com").first()

    assert check_password("S0meFunkyP455", result.password)


def test_can_encode_jwt(encoded_jwt):
    """Tests if JWT can be encoded"""

    assert isinstance(encoded_jwt, bytes)


def test_can_decode_jwt(encoded_jwt):
    """Tests if JWT can be decoded"""

    decoded = decode_jwt(encoded_jwt)

    assert decoded["email"] == "test@test.com"
