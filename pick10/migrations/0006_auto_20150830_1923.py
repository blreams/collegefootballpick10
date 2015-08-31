# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0005_auto_20150823_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='week',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
