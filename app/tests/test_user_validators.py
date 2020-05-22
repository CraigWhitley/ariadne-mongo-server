from modules.core.user.models import User
from modules.core.user.validators import validate_email, validate_user_model, \
                                        validate_password
import pytest
from utils.db import register_test_db


@pytest.fixture(autouse=True)
def setup_db():
    register_test_db()


@pytest.fixture()
def user():
    user = {}
    user["email"] = "correct@email.com"
    user["password"] = "C0rrectP455@"
    user["firstName"] = "Jenny"
    user["lastName"] = "Sandsworth"

    return user


def test_correct_email_validates_true():
    """Tests correct email validates to true"""

    assert validate_email("tem0pdKd@exAmeple.com")


def test_incorrect_email_validates_false():
    """Tests incorrect email validates to false"""

    assert not validate_email("dfgdfggfdsf@fdfsd")


def test_correct_password_validates_true():
    """Tests correct password validates to true"""

    assert validate_password("S1mpl3c0rr3ctP4ss")

    assert validate_password(
        "dfoEs9Y8qnwv6ZcZgCdbhfCAQURLkXDl0PPgODe3PymJmoysRBtWEUmkE4UNPnYD0EJD"
        "5MwKaGjmUHDz6WmAGwJ9otK1Eyus04VWGfuELEPu9iT623uzo1wAi6sKsK3j"
    )


def test_incorrect_passwords_validate_false():
    """Tests incorrect passwords validate to false"""

    assert not validate_password("P4ssw")

    assert not validate_password("passwordovereight")

    assert not validate_password(
        "dfoEs9Y8qnwv6ZcZgCdbhfCAQURLkXDl0PPgODe3PymJmoysRBtWEUmkE4UNPnYD0EJD"
        "5MwKaGjmUHDz6WmAGwJ9otK1Eyus04VWGfuELEPu9iT623udsadsdawAi6sKsK3jsdasd"
    )


def test_user_model_validates(user):
    """Tests user validator returns user after correct validation"""
    User.drop_collection()

    validated_user = validate_user_model(user)

    assert isinstance(validated_user, User)


def test_user_email_already_exists_validation(user):
    """Tests ValueError thrown when email already exists"""

    validated_user = validate_user_model(user)

    validated_user.save()

    with pytest.raises(ValueError):
        validate_user_model(user)
