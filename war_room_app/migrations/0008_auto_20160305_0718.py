# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 07:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('war_room_app', '0007_auto_20160301_0459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='war',
            options={'get_latest_by': 'start_time'},
        ),
    ]
