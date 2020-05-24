from modules.core.user.validators import validate_user_model, \
                                        check_email_exists, \
                                        validate_email, \
                                        validate_password
from modules.core.auth.models import JwtPayload
from modules.core.user.models import User
from modules.core.auth.security import encode_jwt, check_password
import datetime as dt


# TODO: [TEST] auth/user
def register_user(data: dict):
    user = validate_user_model(data)

    token = _get_token(user.email)

    user.access_token = token
    user.updated_at = dt.datetime.utcnow()
    user.save()

    return user


# TODO: [AUTH] Login retry attempts, general login security
def login_user(data: dict):
    email = data["email"]
    password = data["password"]

    if email is None:
        raise ValueError("Email is required.")

    if password is None:
        raise ValueError("Password is required.")

    user = None

    if validate_email(email):
        if check_email_exists(email):
            user = User.objects(email=email).first()
        else:
            raise ValueError("Login incorrect.")
    else:
        raise ValueError("Invalid email.")

    if user is not None:
        if validate_password(password):
            if check_password(password, user.password):
                token = _get_token(email)

                user.access_token = token
                user.updated_at = dt.datetime.utcnow()
                user.save()

                return user
            else:
                raise ValueError("Login incorrect.")
        else:
            raise ValueError("Invalid password.")
    else:
        raise ValueError("Login incorrect")


def _get_token(email: str) -> str:
    """Gets encoded JWT token as a string from email"""
    payload = JwtPayload(email)
    encoded_jwt = encode_jwt(payload.get())

    token = str(encoded_jwt, encoding="utf8")

    return token