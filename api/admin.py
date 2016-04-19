from django.contrib import admin

# Register your models here.
from .models import Course
from .models import DegreeTemplate
from .models import UserDepartment
from .models import UserCourses

admin.site.register(Course)
admin.site.register(DegreeTemplate)
admin.site.register(UserDepartment)
admin.site.register(UserCourses)