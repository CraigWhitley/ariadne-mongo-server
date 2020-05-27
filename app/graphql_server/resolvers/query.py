from ariadne import QueryType, ObjectType
from .user import resolve_all_users, resolve_find_user_by_email, \
                   resolve_me, resolve_get_users_permissions
from .role import resolve_get_all_roles, resolve_get_all_permissions

query = QueryType()


query.set_field("allUsers", resolve_all_users)
query.set_field("findUserByEmail", resolve_find_user_by_email)
query.set_field("me", resolve_me)
query.set_field("getAllRoles", resolve_get_all_roles)
query.set_field("getAllPermissions", resolve_get_all_permissions)
query.set_field("getUsersPermissions", resolve_get_users_permissions)

user = ObjectType("User")
user.set_alias("accessToken", "access_token")

role = ObjectType("Role")
role.set_alias("permissionId", "permission_id")
role.set_alias("roleId", "role_id")