import datetime as dt
from .settings import AuthSettings
from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField
from uuid import uuid4


class JwtPayload:
    """
    Constructs the JWT encoding payload.
    Expiration time (in hours) defaults to 78 hours.
    """
    def __init__(self, email: str,
                 expiration_time=AuthSettings.JWT_EXPIRY,
                 admin=False,
                 issuer=AuthSettings.JWT_ISSUER):

        self.email = email
        self.admin = admin
        self.exp = (dt.datetime.utcnow() +
                    dt.timedelta(hours=expiration_time))
        self.iss = issuer

    def get(self) -> dict:
        payload = {"email": self.email,
                   "admin": self.admin,
                   "exp": self.exp,
                   "iss": self.iss}

        return payload


class BlacklistedToken(Document):
    """Schema to represent a blacklisted token"""
    id = StringField(primary_key=True, default=str(uuid4()))
    token = StringField(max_length=400)
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {"collection": "blacklisted_tokens"}
