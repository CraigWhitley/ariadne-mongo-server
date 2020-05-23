from modules.core.user.models import User
from modules.core.auth.security import authenticate
from modules.core.user.repository import fetch_all_users, \
                                        find_user_by_email, me
# TODO: [RESOLVERS] Add auth to all requests


@authenticate("user:all_users")
def resolve_all_users(_, info, skip=0, take=25) -> list:
    users = fetch_all_users(skip, take)

    return users


@authenticate("user:find_user_by_email")
def resolve_find_user_by_email(_, info, email: str) -> User:
    user = find_user_by_email(email)

    return user

@authenticate("user:me")
def resolve_me(_, info) -> User:
    user = me(info)

    return user
