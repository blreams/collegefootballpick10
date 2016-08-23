# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0010_pick_submit_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('private_name',), 'verbose_name_plural': '2. Players'},
        ),
    ]
