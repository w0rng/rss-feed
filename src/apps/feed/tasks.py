import dramatiq

from apps.feed.models import Feed
from .service.parse_rss import ParseRSS
from django.utils import timezone



@dramatiq.actor
def load_new_posts(feed_pk: int):
    ParseRSS(Feed.objects.get(pk=feed_pk)).save_posts()


def periodically_load_new_posts():
    feeds = Feed.objects.all()
    now = timezone.now()
    for feed in feeds:
        if feed.last_update > now - timezone.timedelta(seconds=feed.interval):
            print(feed.last_update, flush=True)
            print(now - timezone.timedelta(seconds=feed.interval), flush=True)
            print(f"Feed {feed} was updated recently", flush=True)
            continue
        load_new_posts.send(feed.pk)
        feed.last_update = now
        feed.save()
        print(f"Feed {feed} was updated", flush=True)
