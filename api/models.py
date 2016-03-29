from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
	code = models.CharField(max_length=7)
	title = models.CharField(max_length=200)
	instructor = models.CharField(max_length=200)
	prereq = models.CharField(max_length=200)
	description = models.CharField(max_length=1000)
	timings = models.CharField(max_length=200)
	credits = models.IntegerField()

	def __str__(self):
		return self.code