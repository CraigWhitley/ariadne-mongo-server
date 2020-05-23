from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from mongoengine import connect
from dotenv import load_dotenv
import os
# from database.seed import seed_all
from resolvers.query import query, user
from resolvers.mutation import mutation
from modules.core.permissions.permissions_loader import load_all_permissions

load_dotenv()


type_defs = load_schema_from_path("schema/")
schema = make_executable_schema(type_defs, query, mutation, user)


connect(host=os.getenv("MONGO_DEV_URL"), alias='default')


# seed_all()

permissions = load_all_permissions(__file__, "json")

for key in permissions:
    print(key)
    print(permissions[key])

app = GraphQL(schema, debug=True)
