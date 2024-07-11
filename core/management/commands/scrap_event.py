import logging
from datetime import datetime

import requests
import xmltodict
from django.core.management.base import BaseCommand

from core import models as core_models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        url = "https://provider.code-challenge.feverup.com/api/events"

        response = requests.get(url)

        if response.status_code == 200:
            data = xmltodict.parse(response.content)
            self.store_event_data(data)
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch events"))

    def store_event_data(self, event_data):
        self.stdout.write(self.style.SUCCESS("fetch events cron started"))

        logger.info("Storing event data job started ")

        events = event_data["eventList"]["output"]["base_event"]
        for base_event in events:
            if isinstance(base_event["event"], list):
                event_list = base_event["event"]
            else:
                event_list = [base_event["event"]]

            for event in event_list:
                try:
                    start_datetime = datetime.fromisoformat(event["@event_start_date"])
                    end_datetime = datetime.fromisoformat(event["@event_end_date"])
                except ValueError as e:
                    logger.error(f"Invalid date encountered: {e}")
                    continue

                zones = event["zone"]

                if isinstance(zones, dict):
                    zones = [zones]

                prices = [float(zone["@price"]) for zone in zones]
                min_price = min(prices)
                max_price = max(prices)

                core_models.Event.objects.update_or_create(
                    event_number=event["@event_id"],
                    title=base_event["@title"],
                    start_date=start_datetime.date(),
                    start_time=start_datetime.time(),
                    end_date=end_datetime.date(),
                    end_time=end_datetime.time(),
                    min_price=min_price,
                    max_price=max_price,
                )
