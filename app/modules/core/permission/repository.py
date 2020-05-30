from .models import Permission
from uuid import uuid4
from modules.core.validation.service import ValidationService
from typing import List


class PermissionRepository:

    _val_service = ValidationService()

    def get_all_permissions(self) -> List[Permission]:
        return Permission.objects.all()

    def create_new_permission(self, route: str,
                              description: str) -> Permission:

        if self._val_service.validate_permission_route(route) is False:
            raise ValueError("Route is invalid.")

        permission = Permission(
            id=str(uuid4()),
            route=route,
            description=description
        ).save()

        return permission

    def find_permission_by_route(self, route: str) -> Permission:
        
        if self._val_service.validate_permission_route(route) is False:
            raise ValueError("Route is invalid.")

        permission = Permission.objects(route=route).first()

        return permission

    def find_permission_by_id(self, permission_id: str) -> Permission:

        if self._val_service.validate_uuid4(permission_id) is False:
            raise ValueError("Permission ID invalid.")

        permission = Permission.objects(id=permission_id).first()

        return permission
