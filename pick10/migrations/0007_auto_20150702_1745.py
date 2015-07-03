# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0006_auto_20150702_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game_num',
            new_name='gamenum',
        ),
    ]
