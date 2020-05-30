from modules.core.user.models import User
from modules.core.auth.service import authenticate
from modules.core.user.repository import UserRepository
from typing import List

_repo = UserRepository()


@authenticate("user:get_all_users")
def resolve_get_all_users(_, info, skip=0, take=25) -> List[User]:
    users = _repo.get_all_users(skip, take)

    return users


@authenticate("user:add_role_to_user")
def resolve_add_role_to_user(_, info, data: dict) -> User:
    user = _repo.add_role_to_user(data)

    return user


@authenticate("user:find_user_by_email")
def resolve_find_user_by_email(_, info, email: str) -> User:
    user = _repo.find_user_by_email(email)

    return user


@authenticate("user:me")
def resolve_me(_, info) -> User:
    user = _repo.me(info)

    return user


@authenticate("user:get_users_permissions")
def resolve_get_users_permissions(_, info, user_id: str):
    permissions = _repo.get_users_permissions(user_id)

    return permissions


@authenticate("user:update_email")
def resolve_update_email(_, info, data: dict) -> User:
    user = _repo.update_email(data)

    return user


@authenticate("user:add_whitelist_to_user")
def resolve_add_whitelist_to_user(_, info, data: dict) -> User:
    user = _repo.add_whitelist_to_user(data)

    return user


@authenticate("user:add_blacklist_to_user")
def resolve_add_blacklist_to_user(_, info, data: dict) -> User:
    user = _repo.add_blacklist_to_user(data)

    return user


@authenticate("user:delete_blacklist_from_user")
def resolve_delete_blacklist_from_user(_, info, data: dict) -> User:
    user = _repo.delete_blacklist_from_user(data)

    return user


@authenticate("user:delete_whitelist_from_user")
def resolve_delete_whitelist_from_user(_, info, data: dict) -> User:
    user = _repo.delete_whitelist_from_user(data)

    return user

@authenticate("user:update_users_active_status")
def resolve_update_users_active_status(_, info, data: dict) -> User:
    user = _repo.update_users_active_status(data)

    return user
