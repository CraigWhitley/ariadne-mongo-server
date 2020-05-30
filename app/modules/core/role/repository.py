from .models import Role
from modules.core.permission.models import Permission
from uuid import uuid4
from modules.core.validation.service import ValidationService
from typing import List


class RoleRepository:

    _val_service = ValidationService()

    def get_all_roles(self) -> List[Role]:
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

        if count == 0:
            raise ValueError("Role not found. No permissions updated.")

        role = self.find_role_by_id(role_id)

        return role

    def find_role_by_id(self, role_id: str) -> Role:

        if self._val_service.validate_uuid4(role_id) is False:
            raise ValueError("Invalid role ID.")

        role = Role.objects(id=role_id).first()

        return role

    def create_new_role(self, name: str) -> Role:
        if name is None:
            raise ValueError("Role name must be provided.")

        role = Role(
            id=str(uuid4()),
            name=name
        ).save()

        return role
