# Generated by Django 4.2 on 2024-11-04 17:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0038_visitcomponent2_visitcomponent3_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="visitcomponent2",
            old_name="month",
            new_name="month_f",
        ),
        migrations.RenameField(
            model_name="visitcomponent3",
            old_name="month",
            new_name="month_f",
        ),
    ]
