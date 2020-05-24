import enum


class JwtStatus(enum.Enum):
    """Enum to represent the different JWT decode states"""
    EXPIRED = 1
    INVALID_ISSUER = 2
    DECODE_ERROR = 3
