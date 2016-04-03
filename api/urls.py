from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.getCourseData, name='courses'),
    url(r'^courses/(?P<codes>[\w|,]+)/$', views.getCourseData, name='courses'),
    url(r'^update/courses/$', views.updateCourseData, name='update_courses'),
]