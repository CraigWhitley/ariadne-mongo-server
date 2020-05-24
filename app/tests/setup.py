from mongoengine import connect
from modules.core.logging.logger_interface import ILoggingClient
from modules.core.logging.mongo_client import MongoDbLogger
import inject


def service_config(binder):
    binder.bind(ILoggingClient, MongoDbLogger())


def register_test_db():
    connect(alias='default',
            host="mongodb://localhost/maintesoft_test")


def register_test_injections():
    inject.configure(service_config)


def teardown():
    inject.clear()
