import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":

            @receiver(post_migrate)
            def start_scheduler(sender, **kwargs):
                from core.scheduler import start_scheduler

                start_scheduler()
