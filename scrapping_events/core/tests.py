from datetime import datetime

import requests_mock
from core import models as core_models
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class EventModelTestCase(TestCase):
    def setUp(self):
        self.event = core_models.Event.objects.create(
            event_number="291",
            title="Test Event",
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            end_date=datetime.now().date(),
            end_time=datetime.now().time(),
            min_price=10.0,
            max_price=20.0,
        )

    def test_event_creation(self):
        event = core_models.Event.objects.get(event_number="291")
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.min_price, 10.0)
        self.assertEqual(event.max_price, 20.0)


class SearchEventAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = core_models.Event.objects.create(
            event_number="291",
            title="Test Event",
            start_date=datetime(2024, 7, 1).date(),
            start_time=datetime.now().time(),
            end_date=datetime(2024, 7, 10).date(),
            end_time=datetime.now().time(),
            min_price=10.0,
            max_price=20.0,
        )

    def test_search_event_valid_dates(self):
        response = self.client.get(
            reverse("search_event"),
            {"start_date": "2024-07-01", "end_date": "2024-07-10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Event")

    def test_search_event_invalid_date_format(self):
        response = self.client.get(
            reverse("search_event"),
            {"start_date": "2024-07-01", "end_date": "2024-07-32"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.data["error"])

    def test_search_event_missing_dates(self):
        response = self.client.get(reverse("search_event"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please provide start_date and end_date", response.data["error"])


class FetchEventsCommandTestCase(TestCase):
    def setUp(self):
        self.url = "https://provider.code-challenge.feverup.com/api/events"
        self.xml_data = """
        <eventList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        version="1.0" xsi:noNamespaceSchemaLocation="eventList.xsd">
            <output>
                <base_event base_event_id="291" sell_mode="online"
                title="Camela en concierto">
                    <event event_start_date="2021-06-30T21:00:00"
                        event_end_date="2021-06-30T22:00:00"
                        event_id="291" sell_from="2020-07-01T00:00:00"
                        sell_to="2021-06-30T20:00:00" sold_out="false"
                    >
                        <zone zone_id="40" capacity="240"
                        price="20.00" name="Platea" numbered="true"/>
                        <zone zone_id="38" capacity="50"
                        price="15.00" name="Grada 2" numbered="false"/>
                        <zone zone_id="30" capacity="90"
                        price="30.00" name="A28" numbered="true"/>
                    </event>
                </base_event>
                <base_event base_event_id="1591" sell_mode="online"
                    organizer_company_id="1" title="Los Morancos">
                    <event event_start_date="2021-07-31T20:00:00"
                        event_end_date="2021-07-31T21:20:00"
                        event_id="1642" sell_from="2021-06-26T00:00:00"
                        sell_to="2021-07-31T19:50:00" sold_out="false">
                        <zone zone_id="186" capacity="0" price="75.00"
                        name="Amfiteatre" numbered="true"/>
                        <zone zone_id="186" capacity="14" price="65.00"
                        name="Amfiteatre" numbered="false"/>
                    </event>
                </base_event>
                <base_event base_event_id="444" sell_mode="offline"
                    organizer_company_id="1" title="Tributo a Juanito Valderrama">
                    <event event_start_date="2021-09-31T20:00:00"
                    event_end_date="2021-09-31T21:00:00" event_id="1642"
                    sell_from="2021-02-10T00:00:00" sell_to="2021-09-31T19:50:00"
                    sold_out="false">
                        <zone zone_id="7" capacity="22" price="65.00"
                        name="Amfiteatre" numbered="false"/>
                    </event>
                </base_event>
            </output>
        </eventList>
        """

    @requests_mock.Mocker()
    def test_handle_event_fetch_success(self, mocker):
        mocker.get(self.url, text=self.xml_data, status_code=200)
        call_command("scrap_event")
        event = core_models.Event.objects.get(event_number="291")
        self.assertEqual(event.title, "Camela en concierto")
        self.assertEqual(event.min_price, 15.0)
        self.assertEqual(event.max_price, 30.00)
