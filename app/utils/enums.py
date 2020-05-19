import enum


class JwtStatus(enum.Enum):
    """Enum to represent the different JWT decode states"""
    expired = 1
    invalid_issuer = 2
    decode_error = 3
