# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0007_auto_20150307_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='div_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
