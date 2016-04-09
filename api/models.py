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
		return '['+self.code+'] '+self.title

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

class DegreeTemplate(models.Model):
	dept = models.CharField(max_length=7,primary_key=True)
	dept_name = models.CharField(max_length=200)
	IC = models.IntegerField(default=0)
	DC = models.IntegerField(default=0)
	UGP1 = models.IntegerField(default=0)
	UGP2 = models.IntegerField(default=0)
	DE = models.IntegerField(default=0)
	OE = models.IntegerField(default=0)
	SO = models.IntegerField(default=0)
	HSS1 = models.IntegerField(default=0)
	HSS2 = models.IntegerField(default=0)
	total = models.IntegerField(default=0)
	
	def __str__(self):
		return self.dept_name

	def getJSON(self):
		data = {
			'dept' : self.dept,
			'dept_name' : self.dept_name,
			'IC' : self.IC,
			'DC' : self.DC,
			'UGP1' : self.UGP1,
			'UGP2' : self.UGP2,
			'DE' : self.DE,
			'OE' : self.OE,
			'SO' : self.SO,
			'HSS1' : self.HSS1,
			'HSS2' : self.HSS2,
			'total' : self.total
		}
		return data