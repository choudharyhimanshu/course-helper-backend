# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
        migrations.RemoveField(
            model_name='course',
            name='timings',
        ),
        migrations.AddField(
            model_name='course',
            name='credits_distrb',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='course',
            name='dept',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='course',
            name='instr_mail',
            field=models.CharField(default=None, max_length=30),
        ),
        migrations.AddField(
            model_name='course',
            name='instr_notes',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='schedule',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='credits',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='prereq',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
