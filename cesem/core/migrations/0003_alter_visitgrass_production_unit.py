# Generated by Django 4.2 on 2023-05-18 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_visitgrass_visited_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visitgrass",
            name="production_unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.productionunit",
                verbose_name="UP",
            ),
        ),
    ]