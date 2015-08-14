# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='div_name',
            field=models.CharField(default=b'', max_length=40, null=True, blank=True),
        ),
    ]
