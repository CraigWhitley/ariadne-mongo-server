import abc
from .models import LogEntry


class ILoggingClient(metaclass=abc.ABCMeta):
    """Interface that all logging clients must implement"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'log') and
                callable(subclass.log) or
                NotImplemented)

    @abc.abstractmethod
    def log(self,
            entry: LogEntry):
        """Log the error message"""
        raise NotImplementedError
