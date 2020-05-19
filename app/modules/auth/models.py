import datetime as dt


class JwtPayload:
    """
    Constructs the JWT encoding payload.
    Expiration time (in hours) defaults to 78 hours.
    Roles e.g., ['user', 'quotes']
    """
    def __init__(self, email,
                 expiration_time=78,
                 roles=["user"],
                 admin=False,
                 issuer="maintesoft"):

        self.email = email
        self.admin = admin
        self.exp = (dt.datetime.utcnow() +
                    dt.timedelta(hours=expiration_time))
        self.roles = roles
        self.iss = issuer

        # TODO: [SETTINGS] Put certain JWT claims in a settings file, e.g., iss

    def get(self):
        payload = {"email": self.email,
                   "admin": self.admin,
                   "exp": self.exp,
                   "roles": self.roles,
                   "iss": self.iss}

        return payload
