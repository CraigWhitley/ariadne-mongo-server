from .logger_interface import ILoggingClient
from .models import LogEntry, LogLevel
from colorama import Fore, init
import inject
# TODO: [LOG] Have user identifiers in the log?


class LoggingService:
    _client = inject.attr(ILoggingClient)

    def __init__(self,
                 console_output=False,
                 only_console_output=False):
        self._console_output = console_output
        self._only_console_output = only_console_output

    def log(self,
            entry: LogEntry):
        """Log the error with supplied logging client"""
        if self._console_output is True:
            self._console_log(entry)

        if self._only_console_output is True:
            return True

        result = self._client.log(entry)

        if result is not None:
            return result

    def _console_log(self, entry: LogEntry):
        """Log the entry to the console"""

        formatted_entry = self._format_entry(entry)
        init()

        if entry.level == LogLevel.ERROR:
            print(Fore.LIGHTRED_EX + formatted_entry)
        elif entry.level == LogLevel.WARN:
            print(Fore.LIGHTYELLOW_EX + formatted_entry)
        elif entry.level == LogLevel.INFO:
            print(Fore.LIGHTBLUE_EX + formatted_entry)
        elif entry.level == LogLevel.DEBUG:
            print(Fore.LIGHTMAGENTA_EX + formatted_entry)

    def _format_entry(self, entry: LogEntry):
        """Format the log entry into a single-line string"""
        formatted = ("{} - {} "
                     "- {} - {}".format(
                      entry.created_at.strftime(" %H:%M:%S %d-%m-%Y"),
                      entry.level.value,
                      entry.context,
                      entry.message))

        return formatted
