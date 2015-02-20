# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_year', models.IntegerField(default=2015)),
                ('game_week', models.IntegerField(default=1)),
                ('game_num', models.IntegerField(default=0)),
                ('team1_actual_points', models.IntegerField(default=-1)),
                ('team2_actual_points', models.IntegerField(default=-1)),
                ('favored', models.IntegerField(default=0)),
                ('spread', models.IntegerField(default=0)),
                ('game_state', models.IntegerField(default=0)),
                ('quarter', models.CharField(default=b'1st', max_length=3)),
                ('time_left', models.CharField(default=b'15:00', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('team1', models.ForeignKey(related_name=b'team1', to='pick10.Team')),
                ('team2', models.ForeignKey(related_name=b'team2', to='pick10.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
