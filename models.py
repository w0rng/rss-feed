import requests
import urllib3
from feedparser import parse
from tortoise import fields
from tortoise.models import Model


class Feed(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=10240, unique=True)

    async def upgrade(self):
        articles = parse(self.url)['entries']
        for article in articles:
            if not await Article.filter(url=article.link).exists():
                await Article.parse(article.link, self.id)


class Article(Model):
    url = fields.CharField(max_length=10240, unique=True)
    title = fields.TextField()
    paragraphs = fields.JSONField()
    image = fields.TextField()
    tags = fields.JSONField()
    feed = fields.ForeignKeyField('models.Feed', related_name='articles')
    created_at = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def parse(cls, url: str, feed: int):
        try:
            domain = urllib3.util.parse_url(url).host
            summery = requests.get(f'https://functions.yandexcloud.net/d4et1vtk7puk3hij7th2?url={url}').json()
            if 'paragraphs' not in summery:
                return
            newspaper = requests.get(f'https://functions.yandexcloud.net/d4e09pp7rcsn53mvf23j?url={url}').json()
            tags = [domain]
            return await Article.create(url=url, title=summery['title'], paragraphs=paragraphs,
                                        image=newspaper['image'],
                                        tags=tags, feed=feed, created_at=datetime.now())
        except:  # noqa: E722
            print(f"error parse article {url}")


class Read(Model):
    article = fields.ForeignKeyField('models.Article', related_name='reads')
    user = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)


class Bookmark(Model):
    article = fields.ForeignKeyField('models.Article', related_name='bookmarks')
    user = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
