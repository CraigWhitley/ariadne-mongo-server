from modules.core.user.models import User
from modules.core.role.models import Role, Permission
from modules.core.auth.security import hash_password
from uuid import uuid4
from faker import Faker
import random

fake = Faker()
roles = []
permissions = {}


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
                         permissions["get_all_roles"]]
        ).save()
    )

    roles.append(
        Role(
            id=str(uuid4()),
            name="User",
            permissions=[permissions["me"]]
        ).save()
    )


def seed_some_users(amount=50) -> None:
    User(
        id=str(uuid4()),
        email="kiada@test.com",
        password=hash_password("FunkyP455"),
        first_name="Craig",
        last_name="Whitley",
        blacklist=[permissions["find_user_by_email"]],
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
