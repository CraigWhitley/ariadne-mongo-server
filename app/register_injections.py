from modules.core.logging.logger_interface import ILoggingClient
from modules.core.logging.mongo_client import MongoDbLogger


class InjectionService:

    def services_config(self, binder):
        binder.bind(ILoggingClient, MongoDbLogger())
