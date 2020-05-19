from mongoengine import Document, EmailField, StringField, DateTimeField
import datetime as dt
from uuid import uuid4


class User(Document):
    """Schema to represent a user in the database"""
    id = StringField(primary_key=True, default=str(uuid4()))
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=128, min_length=7, required=True)
    first_name = StringField(max_length=50, min_length=2)
    last_name = StringField(max_length=50, min_length=2)
    access_token = StringField(max_length=400)
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())

# TODO: [ROLES] Implement Roles.
