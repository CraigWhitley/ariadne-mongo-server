from modules.core.role.repository import RoleRepository
from modules.core.role.models import Role

_repo = RoleRepository()


def resolve_get_all_roles(_, info):
    roles = _repo.get_all_roles()

    return roles


def resolve_add_permission_to_role(_, info, data: dict):
    role = _repo.add_permission_to_role(data)

    return role


def resolve_add_role_to_user(_, info, data: dict):
    user = _repo.add_role_to_user(data)

    return user


def resolve_get_all_permissions(_, info):
    permissions = _repo.get_all_permission()

    return permissions


def resolve_add_new_role(_, info, name: str) -> Role:
    role = _repo.create_new_role(name)

    return role
