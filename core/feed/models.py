import re
from datetime import datetime
from urllib.parse import urlparse

import requests
from django.db import models, IntegrityError
from django.utils.functional import cached_property
from feedparser import parse
from loguru import logger

CLEANR = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
SPLITTER = re.compile(r"<\s?br\s?/?>")


class Feed(models.Model):
    url = models.URLField(unique=True, max_length=10240)
    title = models.TextField(null=True, default=None, editable=False)

    def load_articles(self):
        logger.warning(f"load articles for feed {self.pk}")
        feed = parse(self.url)
        if self.title is None:
            self.title = feed.feed.title
            self.save()
        exists = set(Article.objects.all().values_list("url", flat=True))
        for article in feed.entries:
            if article.link in exists:
                continue
            Article.parse(article, self)

    def __str__(self):
        return str(self.title)


class Article(models.Model):
    STOP_WORDS = ["курс", "erid", "реклама", "bridge returned error"]

    url = models.URLField(unique=True, max_length=10240)
    title = models.TextField()
    paragraphs = models.JSONField()
    image = models.URLField(max_length=10240, null=True, default=None)
    tags = models.JSONField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="articles")
    created_at = models.DateTimeField()

    @classmethod
    def parse(cls, article, feed: Feed):
        paragraphs, title = cls._get_paragraphs(article)
        if paragraphs is None:
            logger.warning(f"not found paragraphs for {article.link}")
            return

        newspaper = requests.get(f"https://functions.yandexcloud.net/d4e09pp7rcsn53mvf23j?url={article.link}").json()

        tags = [urlparse(article.link).netloc]

        try:
            date = article["published"]
            date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        except:
            date = datetime.now()

        try:
            obj, created = cls.objects.get_or_create(
                url=article.link,
                title=title or paragraphs[0],
                paragraphs=paragraphs,
                image=newspaper.get("image"),
                tags=tags,
                feed=feed,
                created_at=date,
            )
        except IntegrityError:
            logger.exception(article.link)
            return

        if created:
            logger.info(f"add {obj}")
        else:
            logger.info(f"article alredy exists {obj}")

    @classmethod
    def _get_paragraphs(cls, article) -> tuple[list[str] | None, str | None]:
        summery_raw = requests.get(f"https://functions.yandexcloud.net/d4et1vtk7puk3hij7th2?url={article.link}").json()
        if summery := summery_raw.get("paragraphs"):
            return summery, summery_raw.get("title")

        def cleanhtml(raw_html):
            return re.sub(CLEANR, "", raw_html)

        try:
            return list(map(cleanhtml, filter(str, re.split(SPLITTER, article.summary)))), article.get("title")
        except:
            return None, None

    def __str__(self):
        return self.title

    @property
    def count_read(self):
        return self.reads.count()

    @property
    def is_video(self):
        return "youtube" in self.url

    @property
    def video_url(self):
        if "youtube" in self.url:
            return self.url.replace("watch?v=", "embed/")
        return self.url

    @cached_property
    def is_bad(self):
        if self.is_video:
            return False
        for word in self.STOP_WORDS:
            if word.lower() in self.title.lower():
                return True
            for paragraph in self.paragraphs:
                if word.lower() in paragraph.lower():
                    return True
        return False


class Read(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="reads")
    user = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
