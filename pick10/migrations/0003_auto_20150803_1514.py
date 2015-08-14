# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0002_auto_20150802_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='quarter',
            field=models.CharField(default=b'', max_length=3),
        ),
        migrations.AlterField(
            model_name='game',
            name='time_left',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
