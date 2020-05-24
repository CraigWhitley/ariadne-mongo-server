from .models import DbLogEntry, LogEntry
from uuid import uuid4
from .logger_interface import ILoggingClient


class MongoDbLogger(ILoggingClient):

    def log(self,
            entry: LogEntry) -> DbLogEntry:
        """Log the entry into mongodb"""

        log = DbLogEntry(
            id=str(uuid4()),
            level=entry.level.value,
            context=entry.context,
            message=entry.message,
            created_at=entry.created_at
        )

        return log.save()
