from ariadne import MutationType
from .auth import resolve_register_user


mutation = MutationType()
mutation.set_field("registerUser", resolve_register_user)
