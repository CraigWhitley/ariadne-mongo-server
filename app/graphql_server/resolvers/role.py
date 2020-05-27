from modules.core.role.repository import RoleRepository
from modules.core.role.models import Role
from modules.core.auth.service import authenticate

_repo = RoleRepository()


@authenticate("role:get_all_roles")
def resolve_get_all_roles(_, info):
    roles = _repo.get_all_roles()

    return roles


@authenticate("role:get_all_permissions")
def resolve_get_all_permissions(_, info):
    permissions = _repo.get_all_permission()

    return permissions


@authenticate("role:add_permission_to_role")
def resolve_add_permission_to_role(_, info, data: dict):
    role = _repo.add_permission_to_role(data)

    return role


@authenticate("role:add_role_to_user")
def resolve_add_role_to_user(_, info, data: dict):
    user = _repo.add_role_to_user(data)

    return user


@authenticate("role:create_new_role")
def resolve_create_new_role(_, info, name: str) -> Role:
    role = _repo.create_new_role(name)

    return role


@authenticate("role:create_new_permission")
def resolve_create_new_permission(_, info, route: str, description: str):
    permission = _repo.create_new_permission(route, description)

    return permission
