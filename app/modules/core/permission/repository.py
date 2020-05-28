from .models import Permission
from uuid import uuid4


class PermissionRepository:

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
