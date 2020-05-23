from mongoengine import Document, StringField, DateTimeField, \
                        ListField, ReferenceField
import datetime as dt
from uuid import uuid4


class Permission(Document):
    id = StringField(primary_key=True, default=str(uuid4()))
    route = StringField(required=True, max_length=100)
    description = StringField(required=True, max_length=1000)
    meta = {'collection': 'permissions'}


class Role(Document):
    id = StringField(primary_key=True, default=str(uuid4()))
    name = StringField(required=True, unique=True, max_length=100)
    permissions = ListField(ReferenceField(Permission))
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {'collection': 'roles'}
