from mongoengine import Document, StringField
from uuid import uuid4


class Permission(Document):
    id = StringField(primary_key=True, default=str(uuid4()))
    route = StringField(required=True, max_length=100)
    description = StringField(required=True, max_length=1000)
    meta = {'collection': 'permissions'}