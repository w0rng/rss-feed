from logging import getLogger

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand

from feed.models import Feed

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.warning("Starting scheduler")
        scheduler = BlockingScheduler()
        scheduler.add_job(
            self.upgrade_feeds,
            CronTrigger.from_crontab("* * * * *"),
        )
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()

    def upgrade_feeds(self):
        for feed in Feed.objects.all():
            logger.warning(f"Updating feed {feed.id}")
            feed.load_articles()
