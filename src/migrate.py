import peewee as pw

from feed.models import Feed, Article, Read, Bookmark

db = pw.SqliteDatabase('my_database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class FeedOld(BaseModel):
    url = pw.CharField(unique=True)

    class Meta:
        table_name = 'feed'


class ArticleOld(BaseModel):
    url = pw.CharField(unique=True)
    title = pw.CharField()
    paragraphs = pw.TextField()
    image = pw.CharField()
    tags = pw.TextField()
    feed = pw.ForeignKeyField(FeedOld, backref='articles')
    created_at = pw.DateTimeField()

    class Meta:
        table_name = 'article'


class ReadOld(BaseModel):
    article = pw.ForeignKeyField(ArticleOld, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()

    class Meta:
        table_name = 'read'


class SaveOld(BaseModel):
    article = pw.ForeignKeyField(ArticleOld, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()

    class Meta:
        table_name = 'save'


db.connect()
db.create_tables([ArticleOld, FeedOld, ReadOld, SaveOld])

for feed in FeedOld.select():
    if Feed.objects.filter(id=feed.id).exists():
        continue
    Feed(url=feed.url).save()

for article in ArticleOld.select():
    if Article.objects.filter(url=article.url).exists():
        continue
    feed = Feed.objects.filter(url=article.feed.url).first()
    Article(url=article.url, title=article.title, paragraphs=article.paragraphs.split('__'),
            image=article.image,
            tags=article.tags.split('__'), feed=feed, created_at=article.created_at,
            id=article.id).save()
for read in ReadOld.select():
    if Read.objects.filter(id=read.id).exists():
        continue
    article = Article.objects.filter(url=read.article.url).first()
    Read(article=article, user=read.user, created_at=read.created_at).save()
for save in SaveOld.select():
    if Bookmark.objects.filter(id=save.id).exists():
        continue
    article = Article.objects.filter(url=save.article.url).first()
    Bookmark(article=article, user=save.user, created_at=save.created_at).save()
