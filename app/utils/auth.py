import bcrypt


def hash_password(password):
    """Returns hashed user password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password, hashed_password):
    """Compares users password with hashed password"""
    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return True
    else:
        return False
