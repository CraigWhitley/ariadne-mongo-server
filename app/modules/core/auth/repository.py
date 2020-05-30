from modules.core.validation.service import ValidationService
from modules.core.user.models import User
from .service import AuthService
import datetime as dt


class AuthRepository:

    _val_service = ValidationService()
    _auth_service = AuthService()

    # TODO: [TEST] auth/repository test coverage.
    def register_user(self, data: dict):
        """
        Allows a user to register a new account.
        """
        user = self._val_service.validate_user_model(data)

        token = self._auth_service.get_token(user.email)

        user.access_token = token
        user.updated_at = dt.datetime.utcnow()
        user.save()

        return user

    def login(self, data: dict):
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

        if self._val_service.validate_email(email) is False:
            raise ValueError("Invalid email.")

        if self._val_service.check_email_exists(email) is False:
            raise ValueError("Login incorrect.")

        user = User.objects(email=email).first()

        if user is None:
            raise ValueError("Login incorrect")

        if self._val_service.validate_password(password) is False:
            raise ValueError("Invalid password.")

        if self._auth_service.check_password(password,
                                             user.password) is False:
            raise ValueError("Login incorrect.")

        token = self._auth_service.get_token(email)

        user.access_token = token
        user.updated_at = dt.datetime.utcnow()
        user.save()

        return user

    def logout(self, context: dict) -> bool:
        """
        Clear a users JWT token on logout.
        """
        token = self._auth_service.get_token_from_request_header(context)

        self._auth_service.blacklist_token(token)

        user = self._auth_service.get_user_from_token(token)

        user.access_token = ""
        user.updated_at = dt.datetime.utcnow()

        saved_user = user.save()

        if saved_user.access_token == "":
            return True
        else:
            return False
