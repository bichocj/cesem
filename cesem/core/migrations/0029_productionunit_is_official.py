# Generated by Django 4.2 on 2023-11-28 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0028_remove_activity_is_component_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="productionunit",
            name="is_official",
            field=models.BooleanField(default=True, verbose_name="es oficial?"),
        ),
    ]
