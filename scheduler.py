from logging import getLogger

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from models_old import Feed

logger = getLogger(__name__)


def upgrade_feeds():
    feeds = Feed.select()
    for feed in feeds:
        logger.warning(f"Updating feed {feed.id}")
        feed.upgrade()


if __name__ == "__main__":
    logger.warning("Starting scheduler")
    scheduler = BlockingScheduler()
    scheduler.add_job(
        upgrade_feeds,
        CronTrigger.from_crontab("*/5 * * * *"),
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
