from ariadne import MutationType
from .auth import resolve_register_user, resolve_login_user


mutation = MutationType()
mutation.set_field("registerUser", resolve_register_user)
mutation.set_field("loginUser", resolve_login_user)
