# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-10 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20170117_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trend',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='trend',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
