from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_debut', 'date_fin', 'type_conge', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('type_conge', 'is_active', 'date_debut')
    readonly_fields = ('created_at', 'updated_at')
