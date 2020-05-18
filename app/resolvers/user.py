from ariadne import ObjectType
from resolvers.query import query
from user.models import User


user = ObjectType("User")
user.set_alias("firstName", "first_name")
user.set_alias("lastName", "last_name")


@query.field("allUsers")
def resolve_all_users(_, info):
    request = info.context["request"]
    print(request.headers.get("user-agent", "guest"))
    # TODO: add pagination to allUsers resolver
    return User.objects.all()


@query.field("findByEmail")
def resolve_find_by_email(_, info, email):
    print(email)
    request = info.context["request"]
    print(request.headers.get("user-agent", "guest"))
    # TODO: email validation
    return User.objects(email=email).first()