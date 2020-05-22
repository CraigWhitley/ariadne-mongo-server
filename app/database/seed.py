from modules.core.user.models import User
from modules.core.auth.security import hash_password
from uuid import uuid4
from faker import Faker
fake = Faker()


def seed_all() -> None:
    User.drop_collection()
    seed_some_users()

# TODO [FAKER] Write faker framework for re-use throughout tests.


def seed_some_users() -> None:
    for _ in range(75):
        User(
            id=str(uuid4()),
            email=fake.ascii_company_email(),
            password=hash_password(fake.password(length=10,
                                                 digits=True,
                                                 upper_case=True,
                                                 lower_case=True)),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        ).save()
