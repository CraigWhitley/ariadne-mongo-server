import datetime as dt
from settings.app import AppSettings


class JwtPayload:
    """
    Constructs the JWT encoding payload.
    Expiration time (in hours) defaults to 78 hours.
    """
    def __init__(self, email,
                 expiration_time=AppSettings.JWT_EXPIRY,
                 admin=False,
                 issuer=AppSettings.JWT_ISSUER):

        self.email = email
        self.admin = admin
        self.exp = (dt.datetime.utcnow() +
                    dt.timedelta(hours=expiration_time))
        self.iss = issuer

    def get(self):
        payload = {"email": self.email,
                   "admin": self.admin,
                   "exp": self.exp,
                   "iss": self.iss}

        return payload
