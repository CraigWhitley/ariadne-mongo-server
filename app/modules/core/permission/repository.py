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

    def get_permission_from_route(self, route: str) -> Permission:
        # TODO: [VALIDATE] permissions route.
        # Regex tex_t:text

        permission = Permission.objects(route=route).first()

        return permission
