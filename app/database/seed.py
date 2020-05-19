from modules.user.models import User
from utils.auth import hash_password


def seed_all():
    User.drop_collection()
    seed_some_users()


def seed_some_users():
    User(
     email="test@test.com",
     password=hash_password("somethingover8"),
     first_name="Joe",
     last_name="Johnson",
    ).save()

    User(
     email="test2@test.com",
     password=hash_password("somethingover82"),
     first_name="Denny",
     last_name="Johnson",
    ).save()
