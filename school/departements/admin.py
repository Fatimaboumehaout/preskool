from django.contrib import admin
from .models import Departement

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'responsable', 'email', 'created_at')
    search_fields = ('nom', 'code', 'responsable')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
