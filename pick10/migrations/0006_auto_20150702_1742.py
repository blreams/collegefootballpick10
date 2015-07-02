# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0005_auto_20150702_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='week',
            old_name='week_num',
            new_name='weeknum',
        ),
    ]
