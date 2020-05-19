import bcrypt
import jwt
import os
from utils.enums import JwtStatus


def hash_password(password):
    """Returns hashed user password using bcrypt"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password, hashed_password):
    """Compares users password with hashed password"""

    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return True
    else:
        return False


def encode_jwt(payload):
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


def decode_jwt(token):
    """Returns a decoded JWT's payload"""

    key = os.getenv("JWT_SECRET")

    # TODO: [SETTINGS] JWT issuer

    try:
        decoded = jwt.decode(token, key, algorithms='HS256',
                             issuer='maintesoft',
                             options={'require':
                                      ['exp', 'iss', 'email', 'roles']})
    except jwt.ExpiredSignatureError:
        # TODO: [JWT] Refresh token
        return JwtStatus.expired

    except jwt.InvalidIssuerError:
        # TODO: [LOG] Log invalid issuer error
        return JwtStatus.invalid_issuer

    except jwt.InvalidTokenError:
        # TODO: [LOG] Log invalid token error
        return JwtStatus.decode_error

    else:
        return decoded
