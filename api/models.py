from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
	code = models.CharField(max_length=7,unique=True)
	title = models.CharField(max_length=200)
	instructor = models.CharField(max_length=200,default=None)
	instr_mail = models.CharField(max_length=30,default=None)
	prereq = models.CharField(max_length=200,null=True)
	credits = models.IntegerField(default=0)
	credits_distrb = models.CharField(max_length=30,default=None)
	dept = models.CharField(max_length=30,default=None)
	schedule = models.CharField(max_length=200,default=None)
	instr_notes = models.CharField(max_length=1000,null=True)

	def __str__(self):
		return '['+self.code+']'+self.title

	def getJSON(self):
		data = {
			'code' : self.code,
			'title' : self.title,
			'instructor' : self.instructor,
			'instr_mail' : self.instr_mail,
			'prereq' : self.prereq,
			'credits' : self.credits,
			'credits_distrb' : self.credits_distrb,
			'dept' : self.dept,
			'schedule' : self.schedule,
			'instr_notes' : self.instr_notes
		}
		return data
