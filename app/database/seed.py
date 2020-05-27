from modules.core.user.models import User
from modules.core.role.models import Role
from modules.core.permission.models import Permission
from modules.core.auth.service import AuthService
from uuid import uuid4
from faker import Faker
import random

fake = Faker()
roles = []
permissions = {}
permissions_list = []
super_user: Role = None

_auth_service = AuthService()


def seed_all(all_permissions: dict) -> None:
    User.drop_collection()
    Role.drop_collection()
    Permission.drop_collection()
    seed_roles_and_permissions(all_permissions)
    seed_some_users()


def seed_roles_and_permissions(all_permissions: dict, amount=5):

    for data in all_permissions:
        permissions[data] = Permission(
                id=str(uuid4()),
                route=all_permissions[data]["route"],
                description=all_permissions[data]["description"]
        ).save()

    roles.append(
        Role(
            id=str(uuid4()),
            name="Admin",
            permissions=[permissions["all_users"],
                         permissions["me"],
                         permissions["get_users_permissions"],
                         permissions["find_user_by_email"],
                         permissions["get_all_roles"],
                         permissions["add_permission_to_role"],
                         permissions["add_role_to_user"],
                         permissions["get_all_permissions"],
                         permissions["create_new_role"],
                         permissions["create_new_permission"]]
        ).save()
    )

    for data in all_permissions:
        permissions_list.append(
            Permission(
                id=str(uuid4()),
                route=all_permissions[data]["route"],
                description=all_permissions[data]["description"]
            ).save()
        )

    super_user = Role(
            id=str(uuid4()),
            name="SuperUser"
         ).save()

    super_user.update(permissions=permissions_list)

    roles.append(
        Role(
            id=str(uuid4()),
            name="User",
            permissions=[permissions["me"]]
        ).save()
    )


def seed_some_users(amount=50) -> None:
    me = User(
        id=str(uuid4()),
        email="kiada@test.com",
        password=_auth_service.hash_password("FunkyP455"),
        blacklist=[permissions["find_user_by_email"]]
    ).save()

    super_user = Role.objects(name="SuperUser").first()

    me.roles.append(super_user)

    me.save()

    for _ in range(amount):
        role = roles[random.randint(0, len(roles) - 1)]
        User(
            id=str(uuid4()),
            email=fake.ascii_company_email(),
            password=_auth_service.hash_password(fake.password(length=10,
                                                 digits=True,
                                                 upper_case=True,
                                                 lower_case=True)),

            roles=[role]
        ).save()
