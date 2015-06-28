# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0008_userprofile_preferredtz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pick',
            old_name='game_winner',
            new_name='pick_winner',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='pick_week',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='preferredtz',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'US/Alaska', b'US/Alaska'), (b'US/Aleutian', b'US/Aleutian'), (b'US/Arizona', b'US/Arizona'), (b'US/Central', b'US/Central'), (b'US/East-Indiana', b'US/East-Indiana'), (b'US/Eastern', b'US/Eastern'), (b'US/Hawaii', b'US/Hawaii'), (b'US/Indiana-Starke', b'US/Indiana-Starke'), (b'US/Michigan', b'US/Michigan'), (b'US/Mountain', b'US/Mountain'), (b'US/Pacific', b'US/Pacific'), (b'US/Pacific-New', b'US/Pacific-New'), (b'US/Samoa', b'US/Samoa')]),
        ),
    ]
