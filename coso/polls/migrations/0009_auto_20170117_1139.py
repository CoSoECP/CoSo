# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20170116_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='voting_result',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
