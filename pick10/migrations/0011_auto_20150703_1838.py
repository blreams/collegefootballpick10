# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0010_userprofile_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='player',
            field=models.OneToOneField(null=True, blank=True, to='pick10.Player'),
        ),
    ]
