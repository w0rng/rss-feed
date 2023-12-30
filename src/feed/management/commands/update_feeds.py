from logging import getLogger
from time import sleep

from django.core.management.base import BaseCommand

from feed.models import Feed

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.warning("Starting scheduler")
        while True:
            self.upgrade_feeds()
            sleep(10 * 60)

    def upgrade_feeds(self):
        for feed in Feed.objects.all():
            logger.warning(f"Updating feed {feed.id}")
            try:
                feed.load_articles()
            except Exception as e:
                logger.warning(f"Error when update feed {feed.pk}", e)
