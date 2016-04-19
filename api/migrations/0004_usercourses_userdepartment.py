# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160418115013 on 2016-04-19 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_degreetemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(max_length=12, unique=True)),
                ('code', models.CharField(max_length=7, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(max_length=12, unique=True)),
                ('dept', models.CharField(default=None, max_length=30)),
            ],
        ),
    ]
