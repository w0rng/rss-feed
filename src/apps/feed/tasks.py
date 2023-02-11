import dramatiq

from apps.feed.models import Feed
from .service.parse_rss import ParseRSS



@dramatiq.actor
def load_new_posts(feed_pk: int):
    ParseRSS(Feed.objects.get(pk=feed_pk)).save_posts()
