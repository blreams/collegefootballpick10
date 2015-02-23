# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week_year', models.IntegerField()),
                ('week_num', models.IntegerField()),
                ('lock_picks', models.BooleanField(default=False)),
                ('lock_scores', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('winner', models.ForeignKey(to='pick10.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
