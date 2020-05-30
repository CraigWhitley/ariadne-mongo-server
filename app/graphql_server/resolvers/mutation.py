from ariadne import MutationType
from .auth import resolve_register_user, \
                   resolve_login
from .role import resolve_add_permission_to_role, \
                   resolve_create_new_role
from .user import resolve_update_email, \
                    resolve_add_blacklist_to_user, \
                    resolve_add_whitelist_to_user, \
                    resolve_delete_blacklist_from_user, \
                    resolve_delete_whitelist_from_user, \
                    resolve_add_role_to_user
from .permission import resolve_create_new_permission

mutation = MutationType()
mutation.set_field("registerUser", resolve_register_user)
mutation.set_field("login", resolve_login)

mutation.set_field("addPermissionToRole", resolve_add_permission_to_role)
mutation.set_field("addRoleToUser", resolve_add_role_to_user)
mutation.set_field("createNewRole", resolve_create_new_role)

mutation.set_field("createNewPermission", resolve_create_new_permission)

mutation.set_field("updateEmail", resolve_update_email)
mutation.set_field("addWhitelistToUser", resolve_add_whitelist_to_user)
mutation.set_field("addBlacklistToUser", resolve_add_blacklist_to_user)
mutation.set_field("deleteBlacklistFromUser",
                   resolve_delete_blacklist_from_user)
mutation.set_field("deleteWhitelistFromUser",
                   resolve_delete_whitelist_from_user)
