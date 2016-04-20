import json
import urllib2
import os
import pickle
import heapq as hq
import operator

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection
from django.core import serializers
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from api.models import Course
from api.models import DegreeTemplate
from api.models import UserCourses
from api.models import UserDepartment

from bs4 import BeautifulSoup

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

@ensure_csrf_cookie
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

@ensure_csrf_cookie
def updateUserCourses(request):
	directory = "api/data/"
	tracking_pickle = "api/data/tracking.pickle"

	if request.method == 'GET':
		roll = request.GET.get("roll_no", "");
		dept = request.GET.get("dept", "");
		courses = request.GET.get("courses", "");
		return HttpResponse("Hello " + roll + " from " + dept + "!! Welcome to GET update user courses! I got one question: Why are you reading this? You are not supposed to!! Send a POST request!" )
	elif request.method == 'POST':
		roll = request.POST.get("roll_no", "")
		dept = request.POST.get("dept", "");
		courses = request.POST.get("courses", "");
		courses = json.loads(courses)

		# TODO: I must execute the below things using the tables (UserDepartment & UserCourses) in the db (models)
		if not os.path.exists(directory):
			os.makedirs(directory)
		if os.path.exists(tracking_pickle):
			with open(tracking_pickle, "rb") as tracking_file:
				tracking = pickle.load(tracking_file)
		else:
			tracking = dict()
		tracking[roll] = {"dept":dept, 'courses':courses}
		with open(tracking_pickle, "wb") as tracking_file:
			pickle.dump(tracking, tracking_file)

		response = "Hello "+roll+"!! You seem to be from the "+dept+" department!\nWe have saved the courses you have done!"
		return HttpResponse(response)

def recreateGraph(request):
	response = ""
	tracking_pickle = "api/data/tracking.pickle"
	graph_pickle = "api/data/graph.pickle"

	with open(tracking_pickle, "rb") as tracking_file:
		tracking = pickle.load(tracking_file)
	adjMatrix = dict()
	dept_adj = dict()

	for roll_no in tracking.keys():
		dept_adj[tracking[roll_no]['dept']] = dept_adj.get( tracking[roll_no]['dept'], dict() )
		for course in tracking[roll_no]['courses']:
			dept_adj[tracking[roll_no]['dept']][course] = 1 + dept_adj[tracking[roll_no]['dept']].get(course, 0)
			adjMatrix[course] = adjMatrix.get(course, dict())
			for course2 in tracking[roll_no]['courses']:
				adjMatrix[course][course2] = adjMatrix[course].get(course2, 0) + 1

	with open(graph_pickle, "wb") as graph_file:
		pickle.dump((adjMatrix, dept_adj), graph_file)

	response += json.dumps(adjMatrix)
	return HttpResponse(response)

# def updateGraph(request, roll_no):
# 	response = ""
# 	tracking_pickle = "api/data/tracking.pickle"
# 	graph_pickle = "api/data/graph.pickle"

# 	with open(tracking_pickle, "rb") as tracking_file:
# 		tracking = pickle.load(tracking_file)
# 	if os.path.exists(graph_pickle):
# 		with open(graph_pickle, "rb") as graph_file:
# 			adjMatrix, dept_adj = pickle.load(graph_file)
# 	else:
# 		adjMatrix = dict()
# 		dept_adj = dict()

# 	dept_adj[tracking[roll_no]['dept']] = dept_adj.get( tracking[roll_no]['dept'], dict() )
# 	for course in tracking[roll_no]['courses']:
# 		dept_adj[tracking[roll_no]['dept']][course] = 1 + dept_adj[tracking[roll_no]['dept']].get(course, 0)
# 		adjMatrix[course] = adjMatrix.get(course, dict())
# 		for course2 in tracking[roll_no]['courses']:
# 			adjMatrix[course][course2] = adjMatrix[course].get(course2, 0) + 1

# 	with open(graph_pickle, "wb") as graph_file:
# 		pickle.dump((adjMatrix, dept_adj), graph_file)

# 	response += json.dumps(adjMatrix)
# 	return HttpResponse(response)


def dijkstra( adjMatrix, dept, courses):
	distance = dict()
	unvisited = []
	max_score = 0

	for node in adjMatrix.keys():
		max_node = max(adjMatrix[node].values())
		if max_score < max_node:
			max_score = max_node
		if node == dept:
			distance[node] = 0
		elif node in courses:
			distance[node] = 0
			unvisited.append((distance[node], node))
		else:
			distance[node] = float('inf')
			unvisited.append((distance[node], node))

	for node in adjMatrix.keys():
		for neighbor in adjMatrix[node].keys():
			adjMatrix[node][neighbor] = max_score - adjMatrix[node][neighbor] + 1

		if node in courses:
			adjMatrix[dept][node] = 0

	hq.heapify(unvisited)

	# The code for Dijkstra is this
	while unvisited:
		curr = hq.heappop(unvisited)
		for index, node in enumerate(unvisited):
			if node[1] in adjMatrix[curr[1]].keys():
				newDist = curr[0] + adjMatrix[curr[1]][node[1]]
				node = (newDist, node[1]) if (newDist < node[0]) else node
				distance[node[1]] = newDist if (newDist < node[0]) else node[0]
				unvisited[index] = node
		hq.heapify(unvisited)

	# Beautifying the output
	response = sorted(distance.items(), key=operator.itemgetter(1))
	i = 0
	for x in xrange(len(response)):
		if (response[i][0] in courses) or (response[i][0] == dept):
			del response[i]
			i -= 1
		else:
			response[i] = {'course':response[i][0], 'priority':response[i][1]}
		i += 1
	return response

def getGraph(request, roll_no):
	tracking_pickle = "api/data/tracking.pickle"
	graph_pickle = "api/data/graph.pickle"

	with open(tracking_pickle, "rb") as tracking_file:
		tracking = pickle.load(tracking_file)
	tracking = tracking.get(roll_no, None)
	if tracking is None:
		response = "NO GRAPH VALUES for " + roll_no + "\n"
		response += "If you are seeing this, something went wrong!!"
		return HttpResponse(response)
	
	dept = tracking['dept']
	courses = tracking['courses']

	if os.path.exists(graph_pickle):
		response = {}
		response['success'] = True
		with open(graph_pickle, "rb") as graph_file:
			adjMatrix, dept_adj = pickle.load(graph_file)
		adjMatrix[dept] = dept_adj[dept]

		# NOW APPLY DIJKSTRA ON THIS
		ranking = dijkstra( adjMatrix, dept, courses )
		response['data'] = ranking

		return JsonResponse(response)
	
	else:
		response = "NO GRAPH VALUES"
		return HttpResponse(response)