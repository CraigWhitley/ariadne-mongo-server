from validators.user_validation import validate_user_model
from modules.auth.models import JwtPayload
from utils.auth import encode_jwt


def resolve_register_user(_, info, data):
    """
    Resolver for registering a new user
    :param data: The users data to register
    :type data: dict
    :return: UTF8 encoded JWT token
    :rtype: str
    """
    user = validate_user_model(data)

    saved_user = user.save()

    payload = JwtPayload(saved_user.email)
    encoded_jwt = encode_jwt(payload.get())

    token = str(encoded_jwt, encoding="utf8")
    response = {
        "accessToken": token
    }

    return response
