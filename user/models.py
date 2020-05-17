from mongoengine import Document, EmailField, StringField, DateTimeField
import datetime as dt


class User(Document):
    """Schema to represent a user in the db"""
    email = EmailField(required=True)
    password = StringField(max_length=128, min_length=7, required=True,
                           unique=True)
    first_name = StringField(max_length=50, min_length=2)
    last_name = StringField(max_length=50, min_length=2)
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())

