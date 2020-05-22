class UnauthorizedError(Exception):
    """
    Raised when a user tries to access a route not permitted
    by their roles or permissions.
    """
    pass
