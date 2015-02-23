# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0004_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_winner', models.IntegerField(default=0)),
                ('team1_predicted_points', models.IntegerField(default=-1)),
                ('team2_predicted_points', models.IntegerField(default=-1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('pick_game', models.ForeignKey(to='pick10.Game')),
                ('pick_user', models.ForeignKey(to='pick10.User')),
                ('pick_week', models.ForeignKey(to='pick10.Week')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
