from datetime import datetime
from time import mktime
from uuid import uuid4

import feedparser
from apps.feed.models import Feed, Post, Tag
from newspaper import Article


class ParseRSS:
    def __init__(self, feed: Feed):
        self.feed = feed
        self.rss = self._parse_rss(feed.url)

    def get_title(self):
        return self.rss.feed.get("title", str(uuid4()))

    def save_posts(self) -> None:
        for raw_post in self.rss.get("entries", []):
            post, created = Post.objects.get_or_create(
                title=raw_post.title,
                link=raw_post.link,
                feed=self.feed,
                published=datetime.fromtimestamp(mktime(raw_post.published_parsed)),
            )
            if created:
                self._set_post_text(post)
                for tag in self._get_tags(raw_post):
                    post.tags.add(tag.pk)

    def _set_post_text(self, post: Post) -> None:
        article = Article(post.link)
        article.download()
        article.parse()
        if len(article.text) >= 1000:
            article.nlp()
            post.short_post = article.summary
        post.save()

    def _get_tags(self, raw_post: feedparser.FeedParserDict) -> list[Tag]:
        result = []
        for raw_tag in raw_post.tags:
            tag, _ = Tag.objects.get_or_create(name=raw_tag.term)
            result.append(tag)
        return result

    @staticmethod
    def _parse_rss(url):
        return feedparser.parse(url)


"""
from apps.feed.service.parse_rss import ParseRSS
from apps.feed.models import Feed
feed = Feed.objects.first()
parser = ParseRSS(feed)
parser.get_posts()
"""
