from mongoengine import Document, StringField, DateTimeField, \
                        EmbeddedDocumentListField, \
                        EmbeddedDocument
import datetime as dt
from uuid import uuid4


class Permission(EmbeddedDocument):
    route = StringField(required=True, max_length=100)


# TODO: [ROLES] Implement Roles. Embedded document with permissions.
class Role(Document):
    id = StringField(primary_key=True, default=str(uuid4()))
    name = StringField(required=True, unique=True, max_length=100)
    permissions = EmbeddedDocumentListField(Permission)
    blacklist = EmbeddedDocumentListField(Permission)
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {'collection': 'roles'}
