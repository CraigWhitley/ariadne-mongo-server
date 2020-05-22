from modules.core.user.models import User
from modules.core.auth.user import login_user, register_user


def resolve_register_user(_, info, data: dict) -> User:
    """
    Resolver for registering a new user
    :param data: The users data to register
    :type data: dict
    :return: Registered User
    :rtype: User
    """
    user = register_user(data)

    return user


# TODO: [AUTH] Login retry attempts, general login security
def resolve_login_user(_, info, data: dict) -> User:
    """
    Resolver for logging in a user
    """
    user = login_user(data)

    return user
