from time import sleep

from django.core.management.base import BaseCommand
from loguru import logger

from feed.models import Feed


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Starting scheduler")
        while True:
            self.upgrade_feeds()
            sleep(10 * 60)

    def upgrade_feeds(self):
        for feed in Feed.objects.all():
            logger.info(f"Updating feed {feed.id}")
            try:
                feed.load_articles()
            except Exception:
                logger.exception(f"Error when update feed {feed.pk}")
