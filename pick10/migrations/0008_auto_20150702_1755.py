# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0007_auto_20150702_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pick',
            old_name='pick_game',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='pick_player',
            new_name='player',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='pick_winner',
            new_name='winner',
        ),
    ]
