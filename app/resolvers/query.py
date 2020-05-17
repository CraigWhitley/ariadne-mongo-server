from user.models import User
from ariadne import QueryType


query = QueryType()


@query.field("allUsers")
def resolve_all_users(*_):
    return User.objects.all()