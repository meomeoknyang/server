# Generated by Django 5.1.2 on 2024-10-29 07:09

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("baseplace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "place_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("opening_hours", models.CharField(max_length=255)),
                ("image_url", models.URLField(blank=True, max_length=500, null=True)),
                ("contact", models.CharField(blank=True, max_length=15, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("distance_from_gate", models.FloatField(blank=True, null=True)),
                ("open_date", models.DateField(blank=True, null=True)),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="restaurants", to="restaurants.category"
                    ),
                ),
                (
                    "departments",
                    models.ManyToManyField(
                        null=True, related_name="places", to="baseplace.department"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Menu",
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
                ("name", models.CharField(max_length=100)),
                ("price", models.IntegerField()),
                ("description", models.TextField(blank=True)),
                ("image_url", models.URLField(blank=True, max_length=500, null=True)),
                ("is_special", models.BooleanField(default=False)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menus",
                        to="restaurants.restaurant",
                    ),
                ),
            ],
        ),
    ]
