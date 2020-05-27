from modules.core.user.models import User
from modules.core.auth.service import AuthService
import re
from uuid import uuid4


class ValidationService:

    _auth_service = AuthService()

    _email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    # One uppercase, one lowercase, one number. Min 8, max 128.
    _password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,128}$)"

    def validate_user_model(self, user_input: dict) -> User:
        """
        Validates the user model
        """

        id = str(uuid4())
        email = user_input["email"]
        password = user_input["password"]

        if self.check_email_exists(email):
            raise ValueError("Email already exists.")

        if not self.validate_email(email):
            raise ValueError("Valid email not supplied.")

        if not self.validate_password(password):
            raise ValueError("Password must contain 1 uppercase, 1 lowercase, "
                             "and either 1 number or 1 special character.")
        return User(
            id=id,
            email=email,
            password=self._auth_service.hash_password(password)
        )

    def check_email_exists(self, email: str) -> bool:
        """Checks to see if email exists in database"""
        if User.objects(email__iexact=email):
            return True
        else:
            return False

    def validate_email(self, email: str) -> bool:
        """Ensures an email address is in the correct format"""
        return bool(re.match(self._email_regex, email))

    # Password must have at least 8 characters
    # with at least one capital letter,
    # at least one lower case letter and at least one
    # number or special character.
    def validate_password(self, password: str) -> bool:
        """Ensures password meets security requirements:
        min 8, max 128, 1 uppercase, 1 lowercase, 1 number"""
        return bool(re.match(self._password_regex, password))
