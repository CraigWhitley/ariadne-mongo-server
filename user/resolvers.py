from user.models import User
from ariadne import ObjectType


user = ObjectType("User")
user.set_alias("firstName", "first_name")
user.set_alias("lastName", "last_name")