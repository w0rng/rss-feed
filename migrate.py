import peewee as pw

from feed.models import Feed, Article, Read, Bookmark

db = pw.SqliteDatabase('../db/my_database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class FeedOld(BaseModel):
    url = pw.CharField(unique=True)


class ArticleOld(BaseModel):
    url = pw.CharField(unique=True)
    title = pw.CharField()
    paragraphs = pw.TextField()
    image = pw.CharField()
    tags = pw.TextField()
    feed = pw.ForeignKeyField(Feed, backref='articles')
    created_at = pw.DateTimeField()


class ReadOld(BaseModel):
    article = pw.ForeignKeyField(Article, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()


class SaveOld(BaseModel):
    article = pw.ForeignKeyField(Article, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()


def main():
    for feed in FeedOld.select():
        if Feed.objects.filter(id=feed.id).exists():
            continue
        Feed(url=feed.url, id=feed.id).save()
    for article in ArticleOld.select():
        if Article.objects.filter(id=article.id).exists():
            continue
        Article(url=article.url, title=article.title, paragraphs=article.paragraphs.split('__'),
                image=article.image,
                tags=article.tags.split('__'), feed_id=article.feed.id, created_at=article.created_at,
                id=article.id).save()
    for read in ReadOld.select():
        if Read.objects.filter(id=read.id).exists():
            continue
        Read(article_id=read.article.id, user=read.user, created_at=read.created_at, id=read.id).save()
    for save in SaveOld.select():
        if Bookmark.objects.filter(id=save.id).exists():
            continue
        Bookmark(article_id=save.article.id, user=save.user, created_at=save.created_at, id=save.id).save()


if __name__ == '__main__':
    main()
