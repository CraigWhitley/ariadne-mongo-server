from mongoengine import connect
import pytest


@pytest.fixture(autouse=True)
def register_test_db():
    connect(alias='default',
            host="mongodb://localhost/maintesoft_dev")
    connect(alias='test',
            host="mongodb://localhost/maintesoft_test")


def test_db_connections_setup():
    print("Starting tests...")
