# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0004_auto_20150812_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='pick_deadline',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='week',
            name='lock_picks',
            field=models.BooleanField(default=False),
        ),
    ]
