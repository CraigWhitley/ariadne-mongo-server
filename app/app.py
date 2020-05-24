from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from mongoengine import connect
from dotenv import load_dotenv
import os
from database.seed import seed_all
from resolvers.query import query, user
from resolvers.mutation import mutation
from modules.core.permissions.permissions_loader import load_all_permissions
from register_injections import InjectionService
import inject


load_dotenv()

# TODO: [TEST] permissions_loader
# TODO: [TEST] role/repository
# TODO: [TEST] user/repository, validators
# TODO: [DOCS] Go through and make sure everything is documented
# TODO: [LOG] Log all the things!
# TODO: [REFACTOR] Refactor into a more OOP design

type_defs = load_schema_from_path("schema/")
schema = make_executable_schema(type_defs, query, mutation, user)

connect(host=os.getenv("MONGO_DEV_URL"), alias='default')

permissions = load_all_permissions(__file__, "json")

seed_all(permissions)

inject.configure(InjectionService.services_config)

app = GraphQL(schema, debug=True)
