# Generated by Django 4.2 on 2023-06-14 21:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_alter_diagnostic_options_alter_drug_um"),
    ]

    operations = [
        migrations.AddField(
            model_name="visitgrass",
            name="quantity",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=10, verbose_name="cantidad"
            ),
        ),
        migrations.AlterField(
            model_name="visitgrass",
            name="bale",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=10, verbose_name="pacas %"
            ),
        ),
        migrations.AlterField(
            model_name="visitgrass",
            name="ensilage",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=10, verbose_name="ensilado %"
            ),
        ),
        migrations.AlterField(
            model_name="visitgrass",
            name="hay",
            field=models.DecimalField(
                decimal_places=4, default=0, max_digits=10, verbose_name="heno %"
            ),
        ),
        migrations.AlterField(
            model_name="visitgrass",
            name="perennial_grazing",
            field=models.DecimalField(
                decimal_places=4,
                default=0,
                max_digits=10,
                verbose_name="pastoreo perenne %",
            ),
        ),
        migrations.AlterField(
            model_name="visitgrass",
            name="perennial_yield",
            field=models.DecimalField(
                decimal_places=4,
                default=0,
                max_digits=10,
                verbose_name="rendimiento perenne kg",
            ),
        ),
    ]
