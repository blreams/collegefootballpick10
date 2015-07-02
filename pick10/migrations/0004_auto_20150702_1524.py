# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0003_auto_20150702_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('player', models.ForeignKey(to='pick10.Player')),
            ],
            options={
                'verbose_name_plural': '3. PlayerYears',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yearnum', models.IntegerField()),
                ('entry_fee', models.DecimalField(default=10.0, max_digits=6, decimal_places=2)),
                ('first_place', models.DecimalField(default=0.0, max_digits=7, decimal_places=2)),
                ('second_place', models.DecimalField(default=0.0, max_digits=7, decimal_places=2)),
                ('third_place', models.DecimalField(default=0.0, max_digits=7, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '1. Years',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='playeryear',
            name='year',
            field=models.ForeignKey(to='pick10.Year'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='conference',
            options={'verbose_name_plural': '4. Conferences'},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name_plural': '7. Games'},
        ),
        migrations.AlterModelOptions(
            name='pick',
            options={'verbose_name_plural': '8. Picks'},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name_plural': '2. Players'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name_plural': '5. Teams'},
        ),
        migrations.AlterModelOptions(
            name='week',
            options={'verbose_name_plural': '6. Weeks'},
        ),
        migrations.AddField(
            model_name='player',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 15, 23, 52, 478850), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 15, 24, 2, 149698), auto_now=True, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 15, 24, 20, 801054), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 15, 24, 33, 559201), auto_now=True, auto_now_add=True),
            preserve_default=False,
        ),
    ]
