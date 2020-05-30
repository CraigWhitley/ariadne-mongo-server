from modules.core.user.models import User
from modules.core.auth.models import JwtPayload
from modules.core.auth.service import AuthService
import pytest
from uuid import uuid4
from modules.core.user.repository import UserRepository
from modules.core.auth.repository import AuthRepository
from modules.core.auth.settings import AuthSettings
from .setup import register_test_db, register_test_injections, teardown, \
                    drop_all_collections
import jwt
from .mock_models import mock_context


_repo = AuthRepository()
_service = AuthService()
_user_repo = UserRepository()


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()


@pytest.fixture()
def encoded_jwt():
    payload = JwtPayload('test@test.com')

    encoded = _service.encode_jwt(payload.get())

    return encoded


def test_can_authenticate_password():
    """Tests whether a users hashed password can be authenticated"""
    User.drop_collection()
    User(
        id=str(uuid4()),
        email="hashpass@test.com",
        password=_service.hash_password("S0meFunkyP455")
    ).save()
    result = User.objects(email="hashpass@test.com").first()

    assert _service.check_password("S0meFunkyP455", result.password)


def test_can_encode_jwt(encoded_jwt):
    """Tests if JWT can be encoded"""

    assert isinstance(encoded_jwt, bytes)


def test_can_decode_jwt(encoded_jwt):
    """Tests if JWT can be decoded"""
    decoded = _service.decode_jwt(encoded_jwt)

    assert decoded["email"] == "test@test.com"


def test_invalid_jwt_returns_false():
    """Tests invalid JWT returns false"""
    encoded = None

    with pytest.raises(jwt.InvalidTokenError):
        _service.decode_jwt(encoded)


def test_invalid_jwt_iss_returns_false():
    """Tests that JWT decoding require valid issuer"""
    payload = JwtPayload("tes@test.com", AuthSettings.JWT_EXPIRY,
                         False, 'test')
    encoded_jwt = _service.encode_jwt(payload.get())

    with pytest.raises(jwt.InvalidIssuerError):
        _service.decode_jwt(encoded_jwt)


def test_expired_token_returns_false():
    """Tests expired token returns expired status"""
    payload = JwtPayload("test@test.com", -1)
    encoded_jwt = _service.encode_jwt(payload.get())

    with pytest.raises(jwt.ExpiredSignatureError):
        _service.decode_jwt(encoded_jwt)


def test_can_login_user():
    """Tests successful login returns user"""
    user = User(
        id=str(uuid4()),
        email="login@test.com",
        password=_service.hash_password("S0meFunkyP455")
    ).save()

    login_input = {}
    login_input["email"] = user.email
    login_input["password"] = "S0meFunkyP455"

    logged_in_user = _repo.login(login_input)

    assert logged_in_user.access_token is not None


def test_can_retrieve_jwt_string_from_email():
    """
    Tests whether a JWT token can be encoded from an
    email input as a UTF8 string.
    """

    email = "test@test.com"
    jwt_result = _service.get_token(email)

    assert isinstance(jwt_result, str)


def setup_logout_a_user(email: str):
    email = email

    token = _service.get_token(email)

    User(
        id=str(uuid4()),
        email=email,
        password=_service.hash_password("S0m3p4ss"),
        access_token=token).save()

    headers = {
        "authorization": "Bearer " + token
        }

    request = mock_context(headers)

    return request


def test_can_logout():
    request = setup_logout_a_user(email="logout@test.com")

    result = _repo.logout(request.context)

    assert result is True


def test_unauthorized_on_blacklisted_token():
    request = setup_logout_a_user(email="black@test.com")

    _repo.logout(request.context)

    with pytest.raises(ValueError):
        _user_repo.me(request)


def tests_teardown():
    drop_all_collections()
    teardown()
