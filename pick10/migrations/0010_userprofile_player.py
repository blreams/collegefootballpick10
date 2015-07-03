# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0009_auto_20150703_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='player',
            field=models.OneToOneField(default='', to='pick10.Player'),
            preserve_default=False,
        ),
    ]
