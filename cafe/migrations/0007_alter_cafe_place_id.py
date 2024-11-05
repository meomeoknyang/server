# Generated by Django 5.1.2 on 2024-10-29 18:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0006_alter_cafe_place_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cafe",
            name="place_id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]