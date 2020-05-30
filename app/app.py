from dotenv import load_dotenv
import os
from database.seed import seed_all
from modules.core.permission.permissions_loader import load_all_permissions
from config.register_injectors import services_config
import inject
from modules.core.database.db_service import DatabaseService
from modules.core.database.models import ConnectionInput
from graphql_server.server import GraphQLServer

# TODO: [DOCS] Go through and make sure everything is documented
# TODO: [LOG] Log

load_dotenv()

inject.configure(services_config)

connection_input = ConnectionInput(
    hostname=os.getenv("MONGODB_HOSTNAME"),
    db_name="maintesoft",
    alias="default"
)

db_service = DatabaseService()
db_service.connect(connection_input)

permissions = load_all_permissions("json")

seed_all(permissions)

server = GraphQLServer(debug=True)

app = server.get_server()
