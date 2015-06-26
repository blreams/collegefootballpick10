# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0007_auto_20150625_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='preferredtz',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
