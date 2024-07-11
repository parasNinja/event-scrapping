# Generated by Django 5.0.7 on 2024-07-11 13:30

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("event_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("event_number", models.IntegerField()),
                ("title", models.CharField(max_length=255)),
                ("start_date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_date", models.DateField()),
                ("end_time", models.TimeField()),
                ("min_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("max_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
