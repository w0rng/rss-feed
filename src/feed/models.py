from urllib.parse import urlparse

import requests
from django.db import models
from feedparser import parse


class Feed(models.Model):
    url = models.URLField(unique=True)

    def load_articles(self):
        print(f"load articles for feed {self.pk}")
        articles = parse(self.url)['entries']
        for article in articles:
            print(article.link)
            if not Article.objects.filter(url=article.link).exists():
                Article.parse(article.link, self)


class Article(models.Model):
    url = models.URLField(unique=True)
    title = models.TextField()
    paragraphs = models.JSONField()
    image = models.URLField()
    tags = models.JSONField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def parse(cls, url: str, feed: Feed):
        try:
            domain = urlparse(url).netloc
            summery = requests.get(f'https://functions.yandexcloud.net/d4et1vtk7puk3hij7th2?url={url}').json()
            if 'paragraphs' not in summery:
                return
            newspaper = requests.get(f'https://functions.yandexcloud.net/d4e09pp7rcsn53mvf23j?url={url}').json()
            tags = [domain]
            paragraphs = summery['paragraphs']
            return cls.objects.get_or_create(url=url, title=summery['title'], paragraphs=paragraphs,
                                             image=newspaper['image'],
                                             tags=tags, feed=feed)
        except Exception as e:  # noqa: E722
            print(f"error parse article {url}", e)

    def __str__(self):
        return self.title

    @property
    def count_read(self):
        return self.reads.count()


class Read(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reads')
    user = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
