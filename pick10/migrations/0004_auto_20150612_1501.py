# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0003_auto_20150612_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='spread',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=1),
        ),
    ]
