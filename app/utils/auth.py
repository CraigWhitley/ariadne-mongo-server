import bcrypt
import jwt
import os


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
    """Returns an encoded JWT token for supplied payload"""
    key = os.getenv("JWT_SECRET")

    encoded = jwt.encode(payload, key, algorithm='HS256')

    return encoded


def decode_jwt(token):
    """Returns a decoded JWT's payload"""
    # TODO: Catch ExpiredSignatureError and refresh token if required
    key = os.getenv("JWT_SECRET")

    decoded = jwt.decode(token, key, algorithms='HS256')

    return decoded
