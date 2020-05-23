from ariadne import MutationType
from .auth import resolve_register_user, resolve_login_user
from .role import resolve_add_permission_to_role, resolve_add_role_to_user, \
                  resolve_add_new_role

mutation = MutationType()
mutation.set_field("registerUser", resolve_register_user)
mutation.set_field("loginUser", resolve_login_user)
mutation.set_field("addPermissionToRole", resolve_add_permission_to_role)
mutation.set_field("addRoleToUser", resolve_add_role_to_user)
mutation.set_field("addNewRole", resolve_add_new_role)
