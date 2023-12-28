from datetime import datetime

import peewee as pw
import requests
import urllib3
from feedparser import parse

db = pw.SqliteDatabase('db/my_database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Feed(BaseModel):
    url = pw.CharField(unique=True)

    def upgrade(self):
        articles = parse(self.url)['entries']
        for article in articles:
            try:
                Article.get(url=article.link)
            except Article.DoesNotExist:
                Article.parse(article.link, self.id)


class Article(BaseModel):
    url = pw.CharField(unique=True)
    title = pw.CharField()
    paragraphs = pw.TextField()
    image = pw.CharField()
    tags = pw.TextField()
    feed = pw.ForeignKeyField(Feed, backref='articles')
    created_at = pw.DateTimeField()

    @classmethod
    def parse(cls, url: str, feed: int):
        domain = urllib3.util.parse_url(url).host
        summery = requests.get(f'https://functions.yandexcloud.net/d4et1vtk7puk3hij7th2?url={url}').json()
        if 'paragraphs' not in summery:
            return
        newspaper = requests.get(f'https://functions.yandexcloud.net/d4e09pp7rcsn53mvf23j?url={url}').json()
        tags = [domain]
        paragraphs = '__'.join(summery['paragraphs'])
        tags = '__'.join(tags)
        return Article.create(url=url, title=summery['title'], paragraphs=paragraphs, image=newspaper['image'],
                              tags=tags, feed=feed, created_at=datetime.now())


class Read(BaseModel):
    article = pw.ForeignKeyField(Article, backref='reads')
    user = pw.CharField()
    created_at = pw.DateTimeField()
