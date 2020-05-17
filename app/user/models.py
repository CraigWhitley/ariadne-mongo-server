from mongoengine import Document, EmailField, StringField, DateTimeField, \
                        ObjectIdField
import datetime as dt


class User(Document):
    """Schema to represent a user in the db"""
    _id = ObjectIdField()
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=128, min_length=7, required=True)
    first_name = StringField(max_length=50, min_length=2)
    last_name = StringField(max_length=50, min_length=2)
    updated_at = DateTimeField(default=dt.datetime.now())
    created_at = DateTimeField(default=dt.datetime.now())
