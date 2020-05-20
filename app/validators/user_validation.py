from modules.user.models import User
from utils.auth import hash_password
import re
from uuid import uuid4


email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# One uppercase, one lowercase, one number. Min 8, max 128.
password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,128}$)"


def validate_user_model(user_input: dict) -> User:
    """Validates the user model"""
    id = str(uuid4())
    email = user_input["email"]
    password = user_input["password"]

    first_name = None
    last_name = None

    if user_input["firstName"] is not None:
        first_name = user_input["firstName"]

        if len(first_name) < 2 or len(first_name) > 50:
            raise ValueError("First name must be a minimum of 8, maximum "
                             "of 50 characters.")

    if user_input["lastName"] is not None:
        last_name = user_input["lastName"]

        if len(last_name) < 2 or len(last_name) > 50:
            raise ValueError("Last name must be a minimum of 8, maximum "
                             "of 50 characters.")

    if check_email_exists(email):
        raise ValueError("Email already exists.")

    if not validate_email(email):
        raise ValueError("Valid email not supplied.")

    if not validate_password(password):
        raise ValueError("Password must contain 1 uppercase, 1 lowercase, and "
                         "either 1 number or 1 special character.")
    return User(
        id=id,
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name
    )


def check_email_exists(email: str) -> bool:
    """Checks to see if email exists in database"""
    if User.objects(email__iexact=email):
        return True
    else:
        return False


def validate_email(email: str) -> bool:
    """Ensures an email address is in the correct format"""
    return bool(re.match(email_regex, email))


# Password must have at least 8 characters with at least one capital letter,
# at least one lower case letter and at least one number or special character.
def validate_password(password: str) -> bool:
    """Ensures password meets security requirements:
    min 8, max 128, 1 uppercase, 1 lowercase, 1 number"""
    return bool(re.match(password_regex, password))
