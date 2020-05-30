from .models import User
from modules.core.role.repository import RoleRepository
from modules.core.validation.service import ValidationService
from modules.core.auth.service import AuthService
from modules.core.permission.repository import PermissionRepository
import datetime as dt


class UserRepository:

    _val_service = ValidationService()
    _auth_service = AuthService()

    _perm_repo = PermissionRepository()
    _role_repo = RoleRepository()

    _del_blacklist_route = "user:delete_blacklist_from_user"

    def get_all_users(self, skip=0, take=25) -> [User]:
        return User.objects[skip:take+skip]

    def find_user_by_email(self, email: str) -> User:

        if self._val_service.validate_email(email) is False:
            raise ValueError("Invalid email provided.")

        return User.objects(email=email).first()

    def find_user_by_id(self, user_id: str) -> User:

        if self._val_service.validate_uuid4(user_id) is False:
            raise ValueError("Invalid id provided.")

        return User.objects(id=user_id).first()

    def me(self, info) -> User:
        token = self._auth_service.get_token_from_request_header(info.context)

        if token is not None:
            user = self._auth_service.get_user_from_token(token)
            return user

        raise ValueError("User not found.")

    def update_email(self, data: dict) -> bool:

        user_id = data["userId"]
        current_email = data["currentEmail"]
        new_email = data["newEmail"]
        password = data["password"]

        if self._val_service.validate_uuid4(user_id) is False:
            raise ValueError("User id is invalid.")

        if self._val_service.check_user_id_exists(user_id) is False:
            raise ValueError("User not found.")

        if self._val_service.validate_email(current_email) is False:
            raise ValueError("Current email is invalid.")

        if self._val_service.check_email_exists(current_email) is False:
            raise ValueError("Email does not exist.")

        if self._val_service.validate_email(new_email) is False:
            raise ValueError("New email is invalid.")

        if self._val_service.validate_password(password) is False:
            raise ValueError("Password is invalid.")

        user = self.find_user_by_id(user_id)

        if self._auth_service.check_password(password, user.password) is False:
            raise ValueError("Login failed.")

        user.email = new_email

        token = self._auth_service.get_token(new_email)

        self._auth_service.blacklist_token(user.access_token)

        user.access_token = token

        self.update_users_updated_at(user)

        return user

    def get_users_permissions(self, user_id: str) -> dict:
        if self._val_service.validate_uuid4(user_id) is False:
            raise ValueError("Invalid ID.")

        if self._val_service.check_user_id_exists(user_id) is False:
            raise ValueError("User not found.")

        user = self.find_user_by_id(user_id)

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

    def add_role_to_user(self, data: dict) -> User:

        self._val_service.validate_many_uuid4(data)

        user_id = data["userId"]
        role_id = data["roleId"]

        role = self._role_repo.find_role_by_id(role_id)

        if role is None:
            raise ValueError("Role not found.")

        count = User.objects(id=user_id).update_one(add_to_set__roles=role)

        if count == 0:
            raise ValueError("User not found. No roles updated.")

        user = User.objects(id=user_id).first()

        self.update_users_updated_at(user)

        return user

    def add_whitelist_to_user(self, data: dict) -> User:
        new_data = self._get_validated_user_and_permission(data)

        user = new_data["user"]
        permission = new_data["permission"]

        User.objects(id=user.id).update_one(
                                    add_to_set__whitelist=permission)

        user = User.objects(id=user.id).first()

        self.update_users_updated_at(user)

        return user

    def add_blacklist_to_user(self, data: dict) -> User:
        data = self._get_validated_user_and_permission(data)

        user = data["user"]
        permission = data["permission"]

        count = User.objects(id=user.id).update_one(
                                    add_to_set__blacklist=permission)

        if count == 0:
            raise ValueError("No permissions affected.")

        # Ensure that once a user has a blacklisted route, they do not
        # have the ability to remove the blacklists from themselves.
        delete_blacklist = self._perm_repo.find_permission_by_route(
                             self._del_blacklist_route)

        if delete_blacklist not in user.blacklist:
            count = User.objects(id=user.id).update_one(
                                    add_to_set__blacklist=delete_blacklist)
            if count == 0:
                raise ValueError("Unable to add delete_blacklist_from_user.")

        # Return the updated user.
        user = User.objects(id=user.id).first()

        self.update_users_updated_at(user)

        return user

    def delete_whitelist_from_user(self, data: dict) -> User:
        data = self._get_validated_user_and_permission(data)

        user = data["user"]
        permission = data["permission"]

        count = User.objects(id=user.id).update_one(
                                    unset__whitelist=permission)

        if count == 0:
            raise ValueError("Could not remove permission"
                             " from users whitelist.")

        user = self.find_user_by_id(user.id)

        self.update_users_updated_at(user)

        return user

    def update_users_updated_at(self, user):

        user.updated_at = dt.datetime.utcnow()
        user.save()

    def delete_blacklist_from_user(self, data: dict) -> User:
        data = self._get_validated_user_and_permission(data)

        user = data["user"]
        permission = data["permission"]

        count = User.objects(id=user.id).update(
                                    unset__blacklist=permission)

        if count == 0:
            raise ValueError("Could not remove permission"
                             " from users blacklist.")

        user = self.find_user_by_id(user.id)

        # If the only permission left in the users blacklist
        # is the auto-added permission to stop the user removing
        # their own blacklist, remove it.
        permissions_count = len(user.blacklist)

        if permissions_count == 1:
            permission = self._perm_repo.find_permission_by_route(
                            self._del_blacklist_route)

            if self._del_blacklist_route in user.blacklist:
                count = User.objects(id=user.id).update_one(
                                    pull_blacklist=permission)

                if count > 0:
                    user = self.find_user_by_id(user.id)

        self.update_users_updated_at(user)

        return user

    def _get_validated_user_and_permission(self, data: dict) -> dict:
        """
        Helper function to reduce duplicate code in the whitelist
        and blacklist functions.
        """
        user_id = data["userId"]
        permission_id = data["permissionId"]

        if self._val_service.validate_uuid4(user_id) is False:
            raise ValueError("User ID invalid.")

        if self._val_service.validate_uuid4(permission_id) is False:
            raise ValueError("Permission ID invalid.")

        user = self.find_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        permission = self._perm_repo.find_permission_by_id(permission_id)

        if permission is None:
            raise ValueError("Permission not found.")

        result = {}
        result["user"] = user
        result["permission"] = permission

        return result
