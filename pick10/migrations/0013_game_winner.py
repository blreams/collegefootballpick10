# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0012_player_ss_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
