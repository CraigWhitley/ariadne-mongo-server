from .models import Role
from modules.core.permission.models import Permission
from modules.core.user.models import User
from uuid import uuid4
from modules.core.user.validation_service import ValidationService


class RoleRepository:

    _val_service = ValidationService()

    def get_all_roles(self) -> [Role]:
        return Role.objects.all()

    def add_permission_to_role(self, data: dict) -> Role:

        self._val_service.validate_many_uuid4(data)

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

        self._val_service.validate_many_uuid4(data)

        user_id = data["userId"]
        role_id = data["roleId"]

        role = Role.objects(id=role_id).first()

        if role is None:
            raise ValueError("Role not found.")

        count = User.objects(id=user_id).update_one(add_to_set__roles=role)

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
