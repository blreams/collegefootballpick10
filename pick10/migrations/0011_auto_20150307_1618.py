# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0010_auto_20150307_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='winner',
            field=models.ForeignKey(default=None, blank=True, to='pick10.User', null=True),
        ),
    ]
