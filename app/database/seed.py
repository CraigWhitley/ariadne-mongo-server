from user.models import User


def seed_all():
    User.drop_collection()
    seed_some_users()


def seed_some_users():
    User(
     email="test@test.com",
     password="somethingover8",
     first_name="Joe",
     last_name="Johnson",
    ).save()

    User(
     email="test2@test.com",
     password="somethingover82",
     first_name="Denny",
     last_name="Johnson",
    ).save()
