from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from mongoengine import connect
from dotenv import load_dotenv
import os
from database.seed import seed_all
from resolvers.user import user
from resolvers.query import query


load_dotenv()


type_defs = load_schema_from_path("schema/")
schema = make_executable_schema(type_defs, query, user)


def setup_db_connections():
    # Feels pretty awful. Doing this to access this method from
    # test_db_setup.py to configure the test database before running tests.
    # TODO: fix test db connections mess
    connect(host=os.getenv("MONGO_DEV_URL"), alias='default')
    connect(host=os.getenv("MONGO_TEST_URL"), alias='test')


setup_db_connections()
seed_all()


app = GraphQL(schema, debug=True)
