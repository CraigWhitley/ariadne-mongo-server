import inject
from config.register_injectors import services_config
from modules.core.logging.logger_interface import ILoggingClient
from modules.core.logging.mongo_client import MongoDbLogger
from .setup import teardown


class MockDbLogger:
    client = client = inject.attr(ILoggingClient)


def test_can_bind_interfaces():
    inject.configure(services_config)

    logger = MockDbLogger()

    assert isinstance(logger.client, MongoDbLogger)


def finish():
    teardown()
