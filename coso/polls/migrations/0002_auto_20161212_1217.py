# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('birthDate', models.DateTimeField(verbose_name='date published')),
                ('birthPlace', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='DetailedResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteNumber', models.IntegerField(default=0)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('year_in_school', models.CharField(choices=[('FL', 'FarLeft'), ('LE', 'Left'), ('CE', 'Center'), ('RI', 'Right'), ('FR', 'FarRight')], default='CE', max_length=2)),
                ('creationDate', models.DateTimeField(verbose_name='date published')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('score', models.DecimalField(decimal_places=2, max_digits=4)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=4)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Candidate')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Election')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Place')),
            ],
        ),
        migrations.CreateModel(
            name='PollInstitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grade', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votingResult', models.DecimalField(decimal_places=2, max_digits=4)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Candidate')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Election')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginningDate', models.DateTimeField(verbose_name='date published')),
                ('endDate', models.DateTimeField(blank=True, null=True, verbose_name='date published')),
                ('election', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Election')),
                ('positionType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Position')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='pollInstitute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.PollInstitute'),
        ),
        migrations.AddField(
            model_name='detailedresults',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Election'),
        ),
        migrations.AddField(
            model_name='detailedresults',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Place'),
        ),
    ]