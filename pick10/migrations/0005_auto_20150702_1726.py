# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0004_auto_20150702_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='year',
            old_name='first_place',
            new_name='payout_first',
        ),
        migrations.RenameField(
            model_name='year',
            old_name='second_place',
            new_name='payout_second',
        ),
        migrations.RenameField(
            model_name='year',
            old_name='third_place',
            new_name='payout_third',
        ),
        migrations.RemoveField(
            model_name='week',
            name='week_year',
        ),
        migrations.AddField(
            model_name='week',
            name='year',
            field=models.ForeignKey(default='', to='pick10.Year'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='year',
            name='payout_week',
            field=models.DecimalField(default=15.0, max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
