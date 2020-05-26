from modules.core.user.models import User
from modules.core.auth.security import authenticate
from modules.core.user.repository import UserRepository
# TODO: [RESOLVERS] Add auth to all requests

_repo = UserRepository()


@authenticate("user:all_users")
def resolve_all_users(_, info, skip=0, take=25) -> list:
    users = _repo.fetch_all_users(skip, take)

    return users


@authenticate("user:find_user_by_email")
def resolve_find_user_by_email(_, info, email: str) -> User:
    user = _repo.find_user_by_email(email)

    return user


@authenticate("user:me")
def resolve_me(_, info) -> User:
    user = _repo.me(info)

    return user


@authenticate("user:get_users_permissions")
def resolve_get_users_permissions(_, info, email: str):
    permissions = _repo.get_users_permissions(email)

    return permissions
