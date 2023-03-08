from mongoengine import Document, CASCADE
from mongoengine.fields import ReferenceField, ListField, StringField, BooleanField


class Author(Document):
    fullname = StringField(required=True, unique=True, max_length=100)
    born_date = StringField()
    born_location = StringField(max_length=150)
    description = StringField()


class Quote(Document):
    quote = StringField()
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)


class Contact(Document):
    fullname = StringField(required=True, unique=True, max_length=100)
    email = StringField(required=True, unique=True, max_length =100)
    phone = StringField(required=True, unique=True, max_length = 25)
    is_send = BooleanField(default=False)
    message_type = StringField(default='SMS') 
    