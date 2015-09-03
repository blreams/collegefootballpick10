# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0008_auto_20150902_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favorite_team',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
