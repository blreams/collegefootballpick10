# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0009_auto_20150307_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='conf',
            new_name='conference',
        ),
    ]
