# Generated by Django 4.2 on 2025-04-01 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_component3_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='import_in',
            field=models.IntegerField(blank=True, choices=[(0, 'desparasitación')], null=True, verbose_name='importar en'),
        ),
    ]
