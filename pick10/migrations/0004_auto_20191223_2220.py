# Generated by Django 2.2.8 on 2019-12-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0003_playerweekstat_defaulter'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeryear',
            name='first_place',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playeryear',
            name='second_place',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playeryear',
            name='third_place',
            field=models.BooleanField(default=False),
        ),
    ]