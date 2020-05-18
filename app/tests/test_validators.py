from utils.validators import validate_email


def test_correct_email_validates_true():
    """Tests correct email validates to true"""

    assert validate_email("tem0pdKd@exAmeple.com")


def test_incorrect_email_validates_false():
    """Tests incorrect email validates to false"""

    assert not validate_email("dfgdfggfdsf@fdfsd")
