# Generated by Django 4.2 on 2023-11-25 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0026_alter_activity_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="is_component_type",
            field=models.BooleanField(default=False, verbose_name="es componente"),
        ),
    ]
