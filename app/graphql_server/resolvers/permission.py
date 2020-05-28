from modules.core.auth.service import authenticate
from modules.core.permission.repository import PermissionRepository

_repo = PermissionRepository()


@authenticate("role:get_all_permissions")
def resolve_get_all_permissions(_, info):
    permissions = _repo.get_all_permissions()

    return permissions


@authenticate("role:create_new_permission")
def resolve_create_new_permission(_, info, route: str, description: str):
    permission = _repo.create_new_permission(route, description)

    return permission
