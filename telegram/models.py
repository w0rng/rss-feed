from peewee import Model, CharField, PostgresqlDatabase

db = PostgresqlDatabase(
    "postgres",
    user="postgres",
    password="postgres",
    host="db",
)


class User(Model):
    user_id = CharField()

    class Meta:
        database = db


class SentMessage(Model):
    user = CharField()
    message_id = CharField()

    class Meta:
        database = db
