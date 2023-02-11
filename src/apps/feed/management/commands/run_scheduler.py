from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.background import BlockingScheduler
import pytz

from apscheduler.triggers.cron import CronTrigger

from apps.feed.tasks import periodically_load_new_posts


class Command(BaseCommand):
    help = "Run blocking scheduler to create periodical tasks"

    def handle(self, *args, **options):
        print("Preparing scheduler", flush=True)

        scheduler = BlockingScheduler()
        scheduler.add_job(
            periodically_load_new_posts,
            CronTrigger.from_crontab("* * * * *"),
        )

        print("Start scheduler", flush=True)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit, CommandError):
            scheduler.shutdown()
