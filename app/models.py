"""
Contains the database structure.
"""

from datetime import datetime

from bson import ObjectId
from mongoengine import Document, StringField, IntField, DateTimeField


class Url(Document):
    """Define the database structure of a URL."""
    id = ObjectId()
    url = StringField(required=True)
    short_name = StringField(required=True, unique=True)
    short_url = StringField(required=True)
    use_count = IntField(default=0)
    time_created = DateTimeField(default=datetime.utcnow())
    last_accessed = DateTimeField(default=datetime.utcnow())
