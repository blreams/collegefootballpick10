# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0009_auto_20150902_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='pick',
            name='submit_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
