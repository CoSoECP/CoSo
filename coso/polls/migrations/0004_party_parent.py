# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_election_candidates'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Party'),
        ),
    ]