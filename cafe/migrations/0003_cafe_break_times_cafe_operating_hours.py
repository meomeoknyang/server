# Generated by Django 5.1.2 on 2024-10-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("baseplace", "0001_initial"),
        ("cafe", "0002_alter_cafecategory_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="cafe",
            name="break_times",
            field=models.ManyToManyField(
                related_name="cafe_break_times", to="baseplace.breaktime"
            ),
        ),
        migrations.AddField(
            model_name="cafe",
            name="operating_hours",
            field=models.ManyToManyField(
                related_name="cafe_operating_hours", to="baseplace.operatinghours"
            ),
        ),
    ]
