# Generated by Django 5.1.2 on 2024-11-11 16:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_keyword_content_type_keyword_object_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="object_id",
            new_name="place_id",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="content_type",
            new_name="place_type",
        ),
    ]
