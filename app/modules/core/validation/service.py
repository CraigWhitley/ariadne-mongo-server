from modules.core.user.models import User
from modules.core.auth.service import AuthService
import re
from uuid import uuid4


class ValidationService:

    _auth_service = AuthService()

    _email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    _uuid4_regex = r"[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}"

    # this_is_a:valid_route
    _perm_route_regex = r"([a-z_]:?[a-z_])"

    # One uppercase, one lowercase, one number. Min 8, max 128.
    _password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,128}$)"

    def validate_user_model(self, user_input: dict) -> User:
        """ Validates the user model """

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

    def validate_permission_route(self, route: str) -> bool:
        """ Validates the permission route"""

        return bool(re.match(self._perm_route_regex, route))

    def check_email_exists(self, email: str) -> bool:
        """Checks to see if email exists in database"""

        # if User.objects(email__iexact=email) is True:
        #     return True

        # if User.objects(email__match=email) is True:
        #     return True

        # if User.objects(email__exists=email) is True:
        #     return True

        # only one that works correctly: ?

        if User.objects(email=email).first() is not None:
            return True

        return False

    def check_user_id_exists(self, id: str) -> bool:
        """Checks the user exists by id"""

        if User.objects(id__exists=id) is False:
            return False

        return True

    def validate_uuid4(self, id: str) -> bool:
        """Ensures the uuid4 id's are valid"""

        return bool(re.match(self._uuid4_regex, id))

    def validate_many_uuid4(self, data: dict) -> bool:
        for key in data:
            if self.validate_uuid4(data[key]) is False:
                raise ValueError("{} is invalid.".format(key))

        return True

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
