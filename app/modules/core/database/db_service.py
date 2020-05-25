from .models import ConnectionInput
from .database_interface import IDatabaseClient
import inject


class DatabaseService:
    """
    Provides generic database connection functionality.
    """

    _client = inject.attr(IDatabaseClient)

    def connect(self, connection: ConnectionInput):
        """
        Connect to the database in the injected client.
        """
        self._client.connect(connection)

    def disconnect(self, connection: ConnectionInput):
        """
        Disconnect the injected clients database.
        """
        self._client.disconnect(connection)
