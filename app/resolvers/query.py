from ariadne import QueryType, ObjectType
from .user import resolve_all_users, resolve_find_user_by_email

query = QueryType()

query.set_field("allUsers", resolve_all_users)
query.set_field("findUserByEmail", resolve_find_user_by_email)

user = ObjectType("User")
user.set_alias("firstName", "first_name")
user.set_alias("lastName", "last_name")
user.set_alias("accessToken", "access_token")
