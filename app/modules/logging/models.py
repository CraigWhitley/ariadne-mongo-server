from mongoengine import Document, StringField, DateTimeField
import datetime as dt
from uuid import uuid4


class DbLogEntry(Document):
    """Schema to represent a single log entry"""
    id = StringField(primary_key=True, default=str(uuid4()))
    level = StringField(max_length=20, required=True)
    context = StringField(max_length=100)
    message = StringField(max_length=1000, required=True)
    created_at = DateTimeField(default=dt.datetime.now())
    meta = {"collection": "logs"}
