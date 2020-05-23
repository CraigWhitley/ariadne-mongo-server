from modules.core.user.models import User
from modules.core.role.models import Role, Permission
from modules.core.role.permissions import PermissionsList, \
                                          PermissionsDict
from modules.core.auth.security import hash_password
from uuid import uuid4
from faker import Faker
import random

fake = Faker()
roles = []
permissions = []


# TODO [ROLES] Finish off this idea of mixing enums and dict
def seed_all() -> None:
    User.drop_collection()
    Role.drop_collection()
    Permission.drop_collection()
    seed_roles_and_permissions()
    seed_some_users()


def seed_roles_and_permissions(amount=5):

    for per in PermissionsList:
        permissions.append(
            Permission(
                id=str(uuid4()),
                route=per["route"],
                description=per["description"]
            ).save()
        )

    test_perms = {}

    test_perms["get_all_roles"] = Permission(
        id=str(uuid4()),
        route="role:get_all_roles",
        description="Get a list of all roles."
    ).save()

    roles.append(
        Role(
            id=str(uuid4()),
            name="Admin",
            permissions=[permissions[0], permissions[1], permissions[2],
                         test_perms["get_all_roles"]]
        ).save()
    )

    roles.append(
        Role(
            id=str(uuid4()),
            name="User",
            permissions=[permissions[1]]
        ).save()
    )


def seed_some_users(amount=50) -> None:
    User(
        id=str(uuid4()),
        email="kiada@test.com",
        password=hash_password("FunkyP455"),
        first_name="Craig",
        last_name="Whitley",
        blacklist=[permissions[1]],
        roles=[roles[0]]
    ).save()

    for _ in range(amount):
        role = roles[random.randint(0, len(roles) - 1)]
        User(
            id=str(uuid4()),
            email=fake.ascii_company_email(),
            password=hash_password(fake.password(length=10,
                                                 digits=True,
                                                 upper_case=True,
                                                 lower_case=True)),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            roles=[role]
        ).save()
