from ariadne import QueryType, graphql_sync, make_executable_schema, \
                                              load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from mongoengine import connect
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)


type_defs = load_schema_from_path("schema/")


def setup_db_connections():
    connect(host=os.getenv("MONGO_DEV_URL"), alias='default')
    connect(host=os.getenv("MONGO_TEST_URL"), alias='test')


setup_db_connections()


if(__name__) == '__main__':
    app.run(debug=True)
