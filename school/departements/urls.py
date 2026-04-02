from django.urls import path
from . import views

app_name = 'departements'

urlpatterns = [
    path('list/', views.departement_list, name='departement_list'),
    path('add/', views.add_departement, name='add_departement'),
    path('edit/<int:departement_id>/', views.edit_departement, name='edit_departement'),
    path('delete/<int:departement_id>/', views.delete_departement, name='delete_departement'),
]
