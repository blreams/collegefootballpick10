# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0006_auto_20150830_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorite_team',
            field=models.ForeignKey(blank=True, to='pick10.Team', null=True),
            preserve_default=True,
        ),
    ]
