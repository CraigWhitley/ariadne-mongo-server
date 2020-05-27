from mongoengine import Document, EmailField, StringField, DateTimeField, \
                         BooleanField, ListField, ReferenceField, PULL
import datetime as dt
from uuid import uuid4
from modules.core.role.models import Role
from modules.core.permission.models import Permission


class User(Document):
    """Schema to represent a user in the database"""
    id = StringField(primary_key=True, default=str(uuid4()))
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=128, min_length=8, required=True)
    is_active = BooleanField(default=True)
    whitelist = ListField(ReferenceField(Permission, reverse_delete_rule=PULL))
    blacklist = ListField(ReferenceField(Permission, reverse_delete_rule=PULL))
    roles = ListField(ReferenceField(Role, reverse_delete_rule=PULL))
    access_token = StringField(max_length=400)
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {"collection": "users"}
