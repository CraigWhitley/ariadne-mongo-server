import abc
from .models import ConnectionInput


class IDatabaseClient(metaclass=abc.ABCMeta):
    """Interface that all database clients must implement"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'connect') and
                callable(subclass.connect) and
                (hasattr(subclass, 'disconnect') and
                callable(subclass.disconnect) or
                NotImplemented))

    @abc.abstractmethod
    def connect(self, connection: ConnectionInput):
        """Connect to the database"""
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self, connection: ConnectionInput):
        """Disconnect from the database"""
        raise NotImplementedError
