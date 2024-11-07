# Generated by Django 5.1.2 on 2024-11-07 11:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("baseplace", "0002_menu"),
        ("cafe", "0009_remove_cafe_opening_hours_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="breaktime",
            unique_together={("content_type", "object_id")},
        ),
        migrations.DeleteModel(
            name="OperatingHours",
        ),
        migrations.RemoveField(
            model_name="breaktime",
            name="day",
        ),
    ]
