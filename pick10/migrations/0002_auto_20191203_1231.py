# Generated by Django 2.2.7 on 2019-12-03 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick10', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('ss_name', 'private_name'), 'verbose_name_plural': '2. Players'},
        ),
    ]
