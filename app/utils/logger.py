from modules.logging.models import DbLogEntry
import datetime as dt
from uuid import uuid4
import enum
import os, sys


class LogLevel(enum.Enum):
    """Enum to represent the different log levels"""
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARNING"
    ERROR = "ERROR"


class DbLogger:
    def __init__(self,
                 level: LogLevel,
                 context: str,
                 message: str):
        self.level = level.value
        self.context = context
        self.message = message
        self.created_at = dt.datetime.utcnow()

    def save(self) -> DbLogEntry:
        log = DbLogEntry(
            id=str(uuid4()),
            level=self.level,
            context=self.context,
            message=self.message,
            created_at=self.created_at
        )

        return log.save()
