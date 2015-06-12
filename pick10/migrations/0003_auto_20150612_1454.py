# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0002_auto_20150522_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='spread',
            field=models.FloatField(default=0.0),
        ),
    ]
