# Generated by Django 4.2 on 2023-11-25 13:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_activity_is_component_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activity",
            name="is_component_type",
        ),
    ]
