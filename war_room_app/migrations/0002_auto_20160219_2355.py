# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 23:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('war_room_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='war',
            old_name='titles',
            new_name='title',
        ),
    ]
