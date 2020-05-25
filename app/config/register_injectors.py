from modules.core.logging.logger_interface import ILoggingClient
from modules.core.logging.mongo_client import MongoDbLogger
from modules.core.database.database_interface import IDatabaseClient
from modules.core.database.mongo_client import MongoDbClient


def services_config(binder):
    binder.bind(ILoggingClient, MongoDbLogger())
    binder.bind(IDatabaseClient, MongoDbClient())
