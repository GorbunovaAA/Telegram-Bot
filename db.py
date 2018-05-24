from peewee import *


db = SqliteDatabase('people.db')


class Participant(Model):
    name = CharField()
    surname = CharField()
    chat_id = IntegerField()

    class Meta:
        database = db


class Indebtedness(Model):
    from_id = ForeignKeyField(Participant, related_name='from_id')
    to_id = ForeignKeyField(Participant, related_name='to_id')
    chat_id = IntegerField()
    debt = IntegerField(default=0)

    class Meta:
        database = db

db.create_tables([Participant, Indebtedness])
db.close()
