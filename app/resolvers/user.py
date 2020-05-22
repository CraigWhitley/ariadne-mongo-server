from modules.core.user.models import User
from validators.user_validation import validate_email
from modules.core.auth.security import get_token_from_request_header, \
                        get_user_from_token

# TODO: [RESOLVERS] Add auth to all requests


def resolve_all_users(_, info, skip=0, take=25) -> list:
    # TODO: [RESOLVERS] Fix pagination to allUsers resolver. Need to add take onto skip?
    return User.objects[skip:take]


def resolve_find_user_by_email(_, info, email: str) -> User:
    if validate_email(email):
        return User.objects(email=email).first()
    else:
        raise ValueError("Invalid email provided.")


def resolve_me(_, info) -> User:
    token = get_token_from_request_header(info)

    if token is not None:
        user = get_user_from_token(token)
        return user

    raise ValueError("User not found.")
