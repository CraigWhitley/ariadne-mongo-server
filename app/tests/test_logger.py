from modules.logging.client import DbLogger, LogLevel


def test_db_logger_can_save_log():
    """Tests mongodb logger can save a log"""

    log = DbLogger(
        level=LogLevel.ERROR,
        context=__name__,
        message="Testing logger can log"
    ).save()

    assert log.level == "ERROR"
