# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0008_auto_20150307_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='conference',
            name='div_name',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='mascot',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=40),
        ),
    ]
