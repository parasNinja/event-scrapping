import logging
from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import call_command
from django_apscheduler.jobstores import DjangoJobStore, register_events

logger = logging.getLogger(__name__)

scheduler_instance = None


def fetch_events_job():
    logger.info("Running fetch_events_job at %s", datetime.now(pytz.UTC))
    call_command("scrap_event")


def start_scheduler():
    global scheduler_instance

    if scheduler_instance is None:
        timezone = pytz.timezone("UTC")
        scheduler_instance = BackgroundScheduler(timezone=timezone)
        scheduler_instance.add_jobstore(DjangoJobStore(), "default")
        interval_trigger = IntervalTrigger(minutes=1, timezone=timezone)
        scheduler_instance.add_job(
            fetch_events_job,
            interval_trigger,
            name="fetch_events_job",
            jobstore="default",
        )
        register_events(scheduler_instance)
        scheduler_instance.start()
    else:
        logger.info("Scheduler already running")
