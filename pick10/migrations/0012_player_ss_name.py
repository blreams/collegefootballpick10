# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0011_auto_20150703_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='ss_name',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
