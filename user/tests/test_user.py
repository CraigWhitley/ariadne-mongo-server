from user.models import User
from mongoengine.context_managers import switch_db


def test_user_is_created():
    """Tests whether a user can be added to the database"""
    with switch_db(User, 'test'):
        User.drop_collection()
        User(
            email="test@test.com",
            password="somethingover8",
            first_name="Joe",
            last_name="Johnson",
        ).save()
        result = User.objects(email="test@test.com").first()

        assert result.email == "test@test.com"

        # User.drop_collection()
