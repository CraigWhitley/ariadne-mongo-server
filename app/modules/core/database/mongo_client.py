from .database_interface import IDatabaseClient
from .models import ConnectionInput
from mongoengine import connect as conn, disconnect as disc


class MongoDbClient(IDatabaseClient):
    """
    Mongodb client.
    """
    def connect(self, connection: ConnectionInput):
        """
        Connect to the mongodb.
        """
        host = connection.hostname
        alias = connection.alias

        connection_info = {}

        if connection.port is not None:
            connection_info["port"] = connection.port

        if connection.username and connection.password is not None:
            connection_info["username"] = connection.username
            connection_info["password"] = connection.password

        if connection.name is not None:
            connection_info["name"] = connection.name

        # FIXME: [DBCLIENT] Work out how to put the kwargs in
 
        conn(host=host,
             alias=alias)

    def disconnect(self, connection: ConnectionInput):
        """
        Disconnect the mongodb
        """

        disc(alias=connection.alias)
