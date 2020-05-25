class ConnectionInput:
    """
    Model of a generic database connection.
    """
    def __init__(self,
                 hostname: str = "localhost",
                 port: int = None,
                 location: str = None,
                 username: str = None,
                 password: str = None,
                 db_name: str = None,
                 alias: str = "default"):

        self.hostname = hostname
        self.port = port
        self.location = location
        self.username = username
        self.password = password
        self.alias = alias
        self.db_name = db_name
