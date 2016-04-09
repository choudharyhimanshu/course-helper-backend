import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core import serializers

from api.models import Course
from api.models import DegreeTemplate

from bs4 import BeautifulSoup
import urllib2

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the api index.")

def getCourseData(request,codes='all'):
	response = {}
	response['success'] = True

	if codes=='all':
		courses = Course.objects.all()
	else :
		codes = codes.split(',')
		courses = Course.objects.filter(code__in=codes)

	data = []
	for row in courses:
		data.append(row.getJSON())

	response['data'] = {
		'courses' : data,
		'total_courses' : len(data)
	}

	return JsonResponse(response)

def updateCourseData(request):
	START = 0
	LIMIT = 1000
	count = 0

	url = 'http://oars.cc.iitk.ac.in:4040/Common/CourseListing.asp'
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())

	course_codes = soup.find_all('a')

	for code in course_codes:
		if count < START:
			count += 1
			continue
		if count > LIMIT:
			break
		course = code.text.strip()
		course_url = 'http://oars.cc.iitk.ac.in:4040/Utils/CourseInfoPopup2.asp?Course='+course
		course_page = urllib2.urlopen(course_url)
		course_soup = BeautifulSoup(course_page.read())

		cells = course_soup.find_all('td')

		title = cells[3].text.strip()
		instr = cells[5].text.strip()
		instr_mail = cells[7].text.strip()
		prereq = cells[9].text.strip()
		credits_distrb = cells[11].text.strip()
		credits = int(credits_distrb.split('-')[-1])
		dept = cells[13].text.strip()
		schedule = cells[15].text.strip()
		instr_notes = cells[17].text.strip()

		course_model = Course(code=course,title=title,instructor=instr,instr_mail=instr_mail,prereq=prereq,credits=credits,credits_distrb=credits_distrb,dept=dept,schedule=schedule,instr_notes=instr_notes)
		course_model.save()
		print course
		count += 1

	print 'count = ', count
	print 'Last inserted course : %s' % course

def getDegreeTemplate(request,dept='all'):
	response = {}
	response['success'] = True

	if dept=='all':
		templates = DegreeTemplate.objects.all()
	else :
		dept = dept.split(',')
		templates = DegreeTemplate.objects.filter(dept__in=dept)

	data = []
	for row in templates:
		data.append(row.getJSON())

	response['data'] = {
		'template' : data,
		'total_templates' : len(data)
	}

	return JsonResponse(response)