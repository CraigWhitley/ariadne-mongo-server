from mongoengine import register_connection
from app import setup_db_connections
import pytest
import os


@pytest.fixture(autouse=True)
def register_test_db():
    print("Ran db setup")
    register_connection(alias='default',
                        host=os.getenv("MONGO_DEV_URL"))
    register_connection(alias='test',
                        host=os.getenv("MONGO_TEST_URL"))


def test_db_connections_setup():
    setup_db_connections()
