from modules.core.logging.logging_service import LoggingService
from modules.core.logging.models import LogLevel, LogEntry
import pytest
from .setup import register_test_db, register_test_injections, teardown


@pytest.fixture(autouse=True)
def setup():
    register_test_db()
    register_test_injections()


def test_mongo_logging_client_persists_log():
    """
    Test to see if the mongodb client logger
    can persist a log entry to the database
    """

    error_message = "This is a test message."
    logger = LoggingService(console_output=True)

    result = logger.log(LogEntry(LogLevel.ERROR, __name__, error_message))
    logger.log(LogEntry(LogLevel.WARN, __name__, error_message))
    logger.log(LogEntry(LogLevel.INFO, __name__, error_message))
    logger.log(LogEntry(LogLevel.DEBUG, __name__, error_message))

    assert result.message == error_message


def tests_teardown():
    teardown()
