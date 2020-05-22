from modules.core.user.models import User
from modules.core.role.models import Role, Permission
from modules.core.auth.security import hash_password
from uuid import uuid4
from faker import Faker
import random
fake = Faker()
roles = []


def seed_all() -> None:
    User.drop_collection()
    Role.drop_collection()
    seed_roles()
    seed_some_users()


def seed_roles(amount=5):
    permission = Permission(
        route="user:all_users"
    )

    for _ in range(amount):
        roles.append(Role(
            id=str(uuid4()),
            name=fake.word(),
            permissions=[permission],
        ).save())


def seed_some_users(amount=50) -> None:
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
