# Generated by Django 4.2 on 2023-05-18 19:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visitgrass",
            name="visited_at",
            field=models.DateField(
                blank=True, null=True, verbose_name="fecha de creacion"
            ),
        ),
    ]
