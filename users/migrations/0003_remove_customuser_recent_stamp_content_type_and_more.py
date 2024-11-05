# Generated by Django 5.1.2 on 2024-11-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0008_alter_cafe_place_id"),
        ("restaurants", "0008_alter_restaurant_place_id"),
        ("users", "0002_remove_customuser_recent_stamp_restaurants_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="recent_stamp_content_type",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="recent_stamp_object_id",
        ),
        migrations.AddField(
            model_name="customuser",
            name="recent_stamp_cafes",
            field=models.ManyToManyField(
                blank=True, related_name="stamped_by", to="cafe.cafe"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="recent_stamp_restaurants",
            field=models.ManyToManyField(
                blank=True, related_name="stamped_by", to="restaurants.restaurant"
            ),
        ),
    ]
