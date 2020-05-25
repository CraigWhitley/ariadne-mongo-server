from .models import User
from modules.core.user.validation_service import ValidationService
from modules.core.auth.security import get_token_from_request_header, \
                                       get_user_from_token


class UserRepository:

    _validation_service = ValidationService()

    def fetch_all_users(self, skip=0, take=25):
        return User.objects[skip:take+skip]

    def find_user_by_email(self, email: str):
        if self._validation_service.validate_email(email):
            return User.objects(email=email).first()
        else:
            raise ValueError("Invalid email provided.")

    def me(self, info):
        token = get_token_from_request_header(info.context)

        if token is not None:
            user = get_user_from_token(token)
            return user

        raise ValueError("User not found.")

    def get_users_permissions(self, email: str) -> []:
        if self._validation_service.validate_email(email):
            permissions = User.objects(email=email).only('role.permissions')
            print(permissions)
            return permissions
