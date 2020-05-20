import bcrypt
import jwt
import os
from utils.enums import JwtStatus
from settings.app import AppSettings
from utils.logger import DbLogger, LogLevel


def hash_password(password: str) -> str:
    """Returns hashed user password using bcrypt"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: str) -> bool:
    """Compares users password with hashed password"""

    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return True
    else:
        return False


def encode_jwt(payload: dict) -> bytes:
    """
    Returns an encoded JWT token for supplied payload
    :param payload: JWT payload to be encoded
    :type payload: dict
    :return: Encoded JWT token
    :rtype: bytes
    """
    key = os.getenv("JWT_SECRET")

    encoded = jwt.encode(payload, key, algorithm='HS256')

    return encoded


def decode_jwt(token: bytes) -> bytes:
    """Returns a decoded JWT's payload"""

    key = os.getenv("JWT_SECRET")

    try:
        decoded = jwt.decode(token, key, algorithms='HS256',
                             issuer=AppSettings.JWT_ISSUER,
                             options={'require':
                                      ['exp', 'iss', 'email']})
    except jwt.ExpiredSignatureError:
        return JwtStatus.expired

    except jwt.InvalidIssuerError:
        DbLogger(
            LogLevel.ERROR,
            __name__,
            "Attempted to decode token with invalid issuer.").save()
        return JwtStatus.invalid_issuer

    except jwt.InvalidTokenError:
        DbLogger(
            LogLevel.WARN,
            __name__,
            "Attempted to decode an invalid token").save()
        return JwtStatus.decode_error

    else:
        return decoded
