# Generated by Django 5.1.2 on 2024-10-29 11:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurants", "0002_alter_restaurant_departments"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="average_price",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]