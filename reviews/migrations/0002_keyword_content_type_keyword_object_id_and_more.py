# Generated by Django 5.1.2 on 2024-10-29 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="keyword",
            name="content_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="keyword",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="visit_count",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
