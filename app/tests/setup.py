from mongoengine import connect
from modules.core.logging.logger_interface import ILoggingClient
from modules.core.logging.mongo_client import MongoDbLogger
import inject
from modules.core.user.models import User
from modules.core.role.models import Role, Permission
from modules.core.permissions.permissions_loader import load_all_permissions
from uuid import uuid4


def service_config(binder):
    binder.bind(ILoggingClient, MongoDbLogger())


def register_test_db():
    connect(alias='default',
            host="mongodb://localhost/maintesoft_test")
    User.drop_collection()
    Role.drop_collection()
    Permission.drop_collection()


def load_permissions():
    # This doesnt work because windows instead of unix paths?
    permissions = load_all_permissions("json")

    for data in permissions:
        Permission(
            id=str(uuid4()),
            route=permissions[data]["route"],
            description=permissions[data]["description"]
        ).save()


def register_test_injections():
    inject.configure(service_config)


def teardown():
    inject.clear()
