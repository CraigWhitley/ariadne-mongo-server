from modules.user.models import User
from validators.user_validation import validate_email
from utils.auth import decode_jwt, get_token_from_request_header
from utils.logger import DbLogger, LogLevel

# TODO: [RESOLVERS] Add auth to all requests


def resolve_all_users(_, info) -> list:
    # TODO: [RESOLVERS] Add pagination to allUsers resolver
    return User.objects.all()


def resolve_find_user_by_email(_, info, email: str) -> User:
    if validate_email(email):
        return User.objects(email=email).first()
    else:
        raise ValueError("Invalid email provided.")


def resolve_me(_, info) -> User:
    token = get_token_from_request_header(info)

    if token is not None:
        decoded = decode_jwt(token)
        email = decoded["email"]
        user = User.objects(email=email).first()

        if user is not None:
            return user
        else:
            DbLogger(LogLevel.ERROR, __name__,
                     "We decoded a valid token but did not find the user with "
                     "corresponding email in the database!")

    raise ValueError("User not found.")
