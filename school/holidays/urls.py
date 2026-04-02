from django.urls import path
from . import views

app_name = 'holidays'

urlpatterns = [
    path('list/', views.holiday_list, name='holiday_list'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<int:holiday_id>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<int:holiday_id>/', views.delete_holiday, name='delete_holiday'),
]
