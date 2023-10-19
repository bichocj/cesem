# Generated by Django 4.2 on 2023-10-06 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_community_zone_2"),
    ]

    operations = [
        migrations.AddField(
            model_name="sector",
            name="community_2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comunidad_2",
                to="core.community",
                verbose_name="comunidad 2",
            ),
        ),
    ]