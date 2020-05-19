import datetime as dt


class JwtPayload:
    """
    Constructs the JWT encoding payload.
    Expiration time defaults to 78 hours.
    Roles e.g., [Roles.user, Roles.quotes] (??)
    """
    def __init__(self, email,
                 expiration_time=(dt.datetime.utcnow() +
                                  dt.timedelta(hours=78)),
                 roles=["user"],
                 admin=False):

        self.email = email
        self.admin = admin
        self.exp = expiration_time
        self.roles = roles

    def get(self):
        payload = {"email": self.email,
                   "admin": self.admin,
                   "exp": self.exp,
                   "roles": self.roles}

        return payload
