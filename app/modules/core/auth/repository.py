from modules.core.user.validation_service import ValidationService
from modules.core.auth.models import JwtPayload
from modules.core.user.models import User
from .service import AuthService
import datetime as dt


class AuthRepository:

    _validation_service = ValidationService()
    _auth_service = AuthService()

    # TODO: [TEST] auth/repository test coverage. Currently 83%
    def register_user(self, data: dict):
        """
        Allows a user to register a new account.
        """
        user = self._validation_service.validate_user_model(data)

        token = self._get_token(user.email)

        user.access_token = token
        user.updated_at = dt.datetime.utcnow()
        user.save()

        return user

    def login_user(self, data: dict):
        """
        Allows a user to login with email and password.
        """
        email = data["email"]
        password = data["password"]

        if email is None:
            raise ValueError("Email is required.")

        if password is None:
            raise ValueError("Password is required.")

        user = None

        if self._validation_service.validate_email(email):
            if self._validation_service.check_email_exists(email):
                user = User.objects(email=email).first()
            else:
                raise ValueError("Login incorrect.")
        else:
            raise ValueError("Invalid email.")

        if user is not None:
            if self._validation_service.validate_password(password):
                if self._auth_service.check_password(password, user.password):
                    token = self._get_token(email)

                    user.access_token = token
                    user.updated_at = dt.datetime.utcnow()
                    user.save()

                    return user
                else:
                    raise ValueError("Login incorrect.")
            else:
                raise ValueError("Invalid password.")
        else:
            raise ValueError("Login incorrect")

    def _get_token(self, email: str) -> str:
        """
        Gets encoded JWT token as a UTF8 string from email input.
        """
        payload = JwtPayload(email)
        encoded_jwt = self._auth_service.encode_jwt(payload.get())

        token = str(encoded_jwt, encoding="utf8")

        return token

    def logout(self, token: str) -> bool:
        """
        Clear a users JWT token on logout.
        """
        # FIXME: [AUTH] Get the users token from authorization header
        # TODO: [AUTH] blacklist used tokens
        user = self._auth_service.get_user_from_token(token)

        user.access_token = ""

        saved_user = user.save()

        if saved_user.access_token == "":
            return True
        else:
            return False
