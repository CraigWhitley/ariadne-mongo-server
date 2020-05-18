from user.models import User
from utils.auth import hash_password
from utils.validators import validate_email


def resolve_register_user(_, info, data):
    """Resolver for registering a new user"""
    # TODO: Validate incoming user registration
    email = data["email"]
    password = data["password"]

    if User.objects(email__exists=email):
        raise ValueError("Email already exists.")

    if not validate_email(email):
        raise ValueError("Valid email not supplied.")

    first_name = None
    last_name = None

    if data["firstName"] is not None:
        first_name = data["firstName"]

    if data["lastName"] is not None:
        last_name = data["lastName"]

    user = User(
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name
    )

    user.save()
