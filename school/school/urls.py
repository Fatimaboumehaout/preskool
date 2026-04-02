# school/urls.py 
from django.contrib import admin 
from django.urls import path, include 
 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('', include('faculty.urls')), 
    path('student/', include('student.urls')), 
    path('teachers/', include('teachers.urls')),
    path('subjects/', include('subjects.urls')),
    path('exams/', include('exams.urls')),
    path('departements/', include('departements.urls')),
    path('holidays/', include('holidays.urls')),
    path('timetable/', include('timetable.urls')),
    path('authentication/', include('home_auth.urls', namespace='auth')),
    path('dashboard/', include('home_auth.urls')),
]