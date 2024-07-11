# Register your models here.
from django.contrib import admin

from core.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_number",
        "title",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
        "min_price",
        "max_price",
    )
    search_fields = ("event_number", "title")
    list_filter = ("start_date", "end_date")
    date_hierarchy = "start_date"
    ordering = ("-start_date",)


admin.site.register(Event, EventAdmin)
