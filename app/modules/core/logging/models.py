from mongoengine import Document, StringField, DateTimeField
import datetime as dt
from uuid import uuid4
import enum


class DbLogEntry(Document):
    """Schema to represent a single log entry"""
    id = StringField(primary_key=True, default=str(uuid4()))
    level = StringField(max_length=20, required=True)
    context = StringField(max_length=200)
    message = StringField(max_length=1000, required=True)
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {"collection": "logs"}


class LogLevel(enum.Enum):
    """Enum to represent the different log levels"""
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARNING"
    ERROR = "ERROR"


class LogEntry:
    """Class to group log entry inputs"""
    def __init__(self,
                 level: LogLevel,
                 context: str,
                 message: str):

        self.level = level
        self.context = context
        self.message = message
        self.created_at = dt.datetime.utcnow()
