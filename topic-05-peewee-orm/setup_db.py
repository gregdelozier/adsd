from peewee import *

db = SqliteDatabase('pets.db')

class BaseModel(Model):
    class Meta:
        database = db

class Kind(BaseModel):
    kind_name = CharField()
    food = CharField()
    noise = CharField()

class Pet(BaseModel):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref='pets')

# Create tables if they don't exist
db.connect()
db.create_tables([Pet, Kind])