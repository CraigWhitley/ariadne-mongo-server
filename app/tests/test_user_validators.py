from modules.core.user.models import User
from modules.core.user.validation_service import ValidationService
import pytest
from .setup import register_test_db, register_test_injections, teardown,\
                    drop_all_collections
from uuid import uuid4

_service = ValidationService()


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()


@pytest.fixture()
def user():
    user = {}
    user["email"] = "correct@email.com"
    user["password"] = "C0rrectP455@"

    return user


def test_correct_email_validates_true():
    """Tests correct email validates to true"""

    assert _service.validate_email("tem0pdKd@exAmeple.com")


def test_incorrect_email_validates_false():
    """Tests incorrect email validates to false"""

    assert not _service.validate_email("dfgdfggfdsf@fdfsd")


def test_correct_password_validates_true():
    """Tests correct password validates to true"""

    assert _service.validate_password("S1mpl3c0rr3ctP4ss")

    assert _service.validate_password(
        "dfoEs9Y8qnwv6ZcZgCdbhfCAQURLkXDl0PPgODe3PymJmoysRBtWEUmkE4UNPnYD0EJD"
        "5MwKaGjmUHDz6WmAGwJ9otK1Eyus04VWGfuELEPu9iT623uzo1wAi6sKsK3j"
    )


def test_incorrect_passwords_validate_false():
    """Tests incorrect passwords validate to false"""

    assert not _service.validate_password("P4ssw")

    assert not _service.validate_password("passwordovereight")

    assert not _service.validate_password(
        "dfoEs9Y8qnwv6ZcZgCdbhfCAQURLkXDl0PPgODe3PymJmoysRBtWEUmkE4UNPnYD0EJD"
        "5MwKaGjmUHDz6WmAGwJ9otK1Eyus04VWGfuELEPu9iT623udsadsdawAi6sKsK3jsdasd"
    )


def test_user_model_validates(user):
    """Tests user validator returns user after correct validation"""
    User.drop_collection()

    validated_user = _service.validate_user_model(user)

    assert isinstance(validated_user, User)


def test_user_email_already_exists_validation(user):
    """Tests ValueError thrown when email already exists"""

    validated_user = _service.validate_user_model(user)

    validated_user.save()

    with pytest.raises(ValueError):
        _service.validate_user_model(user)


def test_many_uuids_validates_true():
    """
    Tests that validated multiple valid UUID4s
    returns true
    """
    data = {}
    data["someId"] = str(uuid4())
    data["someOtherId"] = str(uuid4())

    assert _service.validate_many_uuid4(data) is True


def tests_teardown():
    drop_all_collections()
    teardown()
