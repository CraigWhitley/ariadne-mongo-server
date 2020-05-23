from modules.core.role.repository import get_all_roles, \
                                         add_permission_to_role, \
                                         add_role_to_user, \
                                         get_all_permission, \
                                         create_new_role
from modules.core.role.models import Role


def resolve_get_all_roles(_, info):
    roles = get_all_roles()

    return roles


def resolve_add_permission_to_role(_, info, data: dict):
    role = add_permission_to_role(data)

    return role


def resolve_add_role_to_user(_, info, data: dict):
    user = add_role_to_user(data)

    return user


def resolve_get_all_permissions(_, info):
    permissions = get_all_permission()

    return permissions


def resolve_add_new_role(_, info, name: str) -> Role:
    role = create_new_role(name)

    return role
