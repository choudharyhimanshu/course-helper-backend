# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7)),
                ('title', models.CharField(max_length=200)),
                ('instructor', models.CharField(max_length=200)),
                ('prereq', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('timings', models.CharField(max_length=200)),
                ('credits', models.IntegerField()),
            ],
        ),
    ]
