from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('subjects/list/', views.subject_list, name='subject_list'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('subject/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subject/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
]
