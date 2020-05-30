from .models import Permission
from uuid import uuid4
from modules.core.user.validation_service import ValidationService


class PermissionRepository:

    _val_service = ValidationService()

    def get_all_permissions(self) -> [Permission]:
        return Permission.objects.all()

    def create_new_permission(self, route: str,
                              description: str) -> Permission:

        new_perm = Permission(
            id=str(uuid4()),
            route=route,
            description=description
        ).save()

        return new_perm

    def get_permission_from_route(self, route: str) -> Permission:
        # TODO: [VALIDATE] permissions route.
        # Regex tex_t:text

        permission = Permission.objects(route=route).first()

        return permission

    def find_permission_by_id(self, permission_id: str) -> Permission:

        if self._val_service.validate_uuid4(permission_id) is False:
            raise ValueError("Permission ID invalid.")

        permission = Permission.objects(id=permission_id).first()

        return permission
