# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20161212_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='candidates',
            field=models.ManyToManyField(through='polls.Result', to='polls.Candidate'),
        ),
    ]
