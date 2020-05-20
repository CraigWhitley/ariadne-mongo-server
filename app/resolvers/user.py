from modules.user.models import User
from validators.user_validation import validate_email


# TODO: [RESOLVERS] Add auth to all requests


def resolve_all_users(_, info: dict) -> list:
    # TODO: [RESOLVERS] add pagination to allUsers resolver
    return User.objects.all()


def resolve_find_user_by_email(_, info, email: str) -> dict:
    if validate_email(email):
        return User.objects(email=email).first()
    else:
        raise ValueError("Invalid email provided.")
