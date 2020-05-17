from user.models import User
from ariadne import ObjectType


user = ObjectType("User")


# @query.field("user")
# def resolve_user():
#     return "Some user"
