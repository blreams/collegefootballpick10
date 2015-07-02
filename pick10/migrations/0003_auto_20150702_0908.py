# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0002_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='pick_user',
        ),
        migrations.AddField(
            model_name='pick',
            name='pick_player',
            field=models.ForeignKey(default='', to='pick10.Player'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='private_name',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='public_name',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
        ),
    ]
