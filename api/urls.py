from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.getCourseData, name='courses'),
    url(r'^courses/(?P<codes>[\w|,]+)/$', views.getCourseData, name='courses'),
    url(r'^update/courses/$', views.updateCourseData, name='update_courses'),
    url(r'^degree-template/$', views.getDegreeTemplate, name='template'),
    url(r'^degree-template/(?P<dept>[\w|,]+)/$', views.getDegreeTemplate, name='template'),
    url(r'^update-user-courses/$', views.updateUserCourses, name='user_courses'),
    url(r'^update-graph/$', views.updateGraph, name='graph'),
]