from rest_framework import serializers

from core import models as core_models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Event
        fields = [
            "event_id",
            "title",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "min_price",
            "max_price",
        ]
