from apps.feed.models import Feed, Post
from apps.user.models import User
from feedgen.feed import FeedGenerator as FeedGen


class FeedGenerator:
    def __init__(self, user: User):
        self.user = user

    def generate(self) -> str:
        feed = FeedGen()
        feed.title(self.user.username)
        feed.author({"name": self.user.username})
        feed.link(href="https://example.com")
        feed.description("RSS feed for user")

        for post in self._get_posts(self._get_feeds()):
            entry = feed.add_entry()
            entry.title(post.title)
            entry.description(post.short_post)
            entry.link(href=post.link)
            entry.category([{"term": tag.name} for tag in post.tags.all()])

            entry.pubDate(post.published)

        return feed.rss_str(pretty=True)

    def _get_feeds(self) -> list[Feed]:
        return Feed.objects.filter(author=self.user)

    def get_post(self, feeds: list[Feed]) -> list[Post]:
        ...

    def _get_posts(self, feeds: list[Feed]) -> list[Post]:
        return (
            Post.objects.filter(feed__in=feeds, published__isnull=False).order_by("-published").prefetch_related("tags")
        )


"""
from apps.user.models import User
from apps.feed.service.generate_feed import FeedGenerator

user = User.objects.first()
generator = FeedGenerator(user)
print(generator.generate())
"""
