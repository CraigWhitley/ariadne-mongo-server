from ariadne import ObjectType
from resolvers.query import query
from user.models import User
from validators.user_validation import validate_email


user = ObjectType("User")
user.set_alias("firstName", "first_name")
user.set_alias("lastName", "last_name")


@query.field("allUsers")
def resolve_all_users(*_):
    # TODO: add pagination to allUsers resolver
    return User.objects.all()


@query.field("findUserByEmail")
def resolve_find_user_by_email(_, info, email):
    if validate_email(email):
        return User.objects(email=email).first()
    else:
        raise ValueError("Invalid email provided.")
