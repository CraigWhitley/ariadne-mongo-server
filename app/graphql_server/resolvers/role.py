from modules.core.role.repository import RoleRepository
from modules.core.role.models import Role
from modules.core.auth.service import authenticate
from typing import List

_repo = RoleRepository()


@authenticate("role:get_all_roles")
def resolve_get_all_roles(_, info) -> List[Role]:
    roles = _repo.get_all_roles()

    return roles


@authenticate("role:add_permission_to_role")
def resolve_add_permission_to_role(_, info, data: dict) -> Role:
    role = _repo.add_permission_to_role(data)

    return role


@authenticate("role:create_new_role")
def resolve_create_new_role(_, info, name: str) -> Role:
    role = _repo.create_new_role(name)

    return role
