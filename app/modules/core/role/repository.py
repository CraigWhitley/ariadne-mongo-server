from .models import Role
from modules.core.permission.models import Permission
from modules.core.user.models import User
from uuid import uuid4


class RoleRepository:

    def get_all_roles(self) -> [Role]:
        return Role.objects.all()

    def get_all_permissions(self) -> [Permission]:
        return Permission.objects.all()

    def add_permission_to_role(self, data: dict) -> Role:

        permission_id = data["permissionId"]
        role_id = data["roleId"]

        permission = Permission.objects(id=permission_id).first()

        if permission is None:
            raise ValueError("Permission not found.")

        count = Role.objects(id=role_id).update_one(
                                         push__permissions=permission)

        role = None

        if count > 0:
            role = Role.objects(id=role_id).first()
        else:
            raise ValueError("Role not found. No permissions updated.")

        return role

    def add_role_to_user(self, data: dict) -> User:
        user_id = data["userId"]
        role_id = data["roleId"]

        if user_id is None:
            raise ValueError("User id must be supplied.")

        if role_id is None:
            raise ValueError("Role id must be supplied")

        role = Role.objects(id=role_id).first()

        if role is None:
            raise ValueError("Role not found.")

        count = User.objects(id=user_id).update_one(push__roles=role)

        if count == 0:
            raise ValueError("User not found. No roles updated.")

        user = User.objects(id=user_id).first()

        return user

    def create_new_role(self, name: str) -> Role:
        if name is None:
            raise ValueError("Role name must be provided.")

        role = Role(
            id=str(uuid4()),
            name=name
        ).save()

        return role

    def create_new_permission(self, route: str,
                              description: str) -> Permission:

        new_perm = Permission(
            id=str(uuid4()),
            route=route,
            description=description
        ).save()

        return new_perm
