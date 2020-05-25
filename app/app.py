from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from dotenv import load_dotenv
import os
from database.seed import seed_all
from graphql_server.resolvers.query import query, user
from graphql_server.resolvers.mutation import mutation
from modules.core.permissions.permissions_loader import load_all_permissions
from register_injections import services_config
import inject
from modules.core.database.db_service import DatabaseService
from modules.core.database.models import ConnectionInput

# TODO: [TEST] permissions_loader
# TODO: [TEST] role/repository
# TODO: [TEST] user/repository, validators
# TODO: [DOCS] Go through and make sure everything is documented
# TODO: [LOG] Log all the things!
# TODO: [REFACTOR] Refactor into a more OOP design

load_dotenv()

inject.configure(services_config)

connection_input = ConnectionInput(
    hostname=os.getenv("MONGO_DEV_URL")
)

db_service = DatabaseService()
db_service.connect(connection_input)

type_defs = load_schema_from_path("graphql_server/schema/")
schema = make_executable_schema(type_defs, query, mutation, user)

permissions = load_all_permissions(__file__, "json")

seed_all(permissions)

app = GraphQL(schema, debug=True)
