from peewee import *
from datetime import datetime


db = SqliteDatabase('people.db')


class Participant(Model):
    name = CharField()
    surname = CharField()
    chat_id = IntegerField()

    class Meta:
        database = db
        # primary_key = CompositeKey('name', 'surname')


class Currency(Model):
    dollar_rate = DoubleField(default=1)

    class Meta:
        database = db


class Indebtedness(Model):
    from_id = ForeignKeyField(Participant, related_name='from_id')
    to_id = ForeignKeyField(Participant, related_name='to_id')
    chat_id = IntegerField()
    debt = IntegerField(default=0)
    star_data = DateField(default=datetime.now())
    expiry_data = DateField(default=datetime.now())
    procent = DoubleField(default=0)
    # currency = ForeignKeyField(Currency, related_name='cur_id')

    class Meta:
        database = db

db.create_tables([Participant, Currency, Indebtedness])
db.close()
