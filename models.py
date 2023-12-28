import peewee as pw

db = pw.SqliteDatabase('db/my_database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Feed(BaseModel):
    url = pw.CharField(unique=True)


class Article(BaseModel):
    url = pw.CharField(unique=True)
    title = pw.CharField()
    paragraphs = pw.TextField()
    image = pw.CharField()
    tags = pw.TextField()
    feed = pw.ForeignKeyField(Feed, backref='articles')
    created_at = pw.DateTimeField()


class Read(BaseModel):
    article = pw.ForeignKeyField(Article, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()
