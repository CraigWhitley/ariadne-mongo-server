from .models import User
from modules.core.user.validation_service import ValidationService
from modules.core.auth.security import AuthService


class UserRepository:

    _validation_service = ValidationService()
    _auth_service = AuthService()

    def fetch_all_users(self, skip=0, take=25):
        return User.objects[skip:take+skip]

    def find_user_by_email(self, email: str):
        if self._validation_service.validate_email(email):
            return User.objects(email=email).first()
        else:
            raise ValueError("Invalid email provided.")

    def me(self, info):
        token = self._auth_service.get_token_from_request_header(info.context)

        if token is not None:
            user = self._auth_service.get_user_from_token(token)
            return user

        raise ValueError("User not found.")

    def get_users_permissions(self, email: str) -> []:
        if self._validation_service.validate_email(email):
            """Returns a list of all a users permissions """
            user = User.objects(email=email).first()

            permissions = {}
            permissions["blacklist"] = []
            permissions["whitelist"] = []
            permissions["permissions"] = []

            if hasattr(user, 'blacklist'):
                for black in user.blacklist:
                    permissions["blacklist"].append(black)

            if hasattr(user, 'whitelist'):
                for white in user.whitelist:
                    permissions["whitelist"].append(white)

            for role in user.roles:
                for perm in role.permissions:
                    permissions["permissions"].append(perm)

            return permissions
