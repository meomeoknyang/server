# Generated by Django 5.1.2 on 2024-10-29 18:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cafe", "0007_alter_cafe_place_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cafe",
            name="place_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]