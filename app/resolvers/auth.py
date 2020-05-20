from validators.user_validation import validate_user_model
from modules.auth.models import JwtPayload
from utils.auth import encode_jwt


def resolve_register_user(_, info, data: dict) -> dict:
    """
    Resolver for registering a new user
    :param data: The users data to register
    :type data: dict
    :return: UTF8 encoded "accessToken" JWT
    :rtype: dict
    """
    user = validate_user_model(data)

    payload = JwtPayload(user.email)
    encoded_jwt = encode_jwt(payload.get())

    token = str(encoded_jwt, encoding="utf8")

    user.access_token = token
    user.save()

    response = {
        "accessToken": token
    }

    return response

# TODO: Login, logout resolvers
