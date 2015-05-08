# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0011_auto_20150307_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conference',
            options={'verbose_name_plural': '1. Conferences'},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name_plural': '3. Games'},
        ),
        migrations.AlterModelOptions(
            name='pick',
            options={'verbose_name_plural': '5. Picks'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name_plural': '2. Teams'},
        ),
        migrations.AlterModelOptions(
            name='week',
            options={'verbose_name_plural': '4. Weeks'},
        ),
    ]
