from django.contrib import admin
from .models import Agence

@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'institution', 'statut')
    list_filter = ('institution', 'statut')
    search_fields = ('id', 'nom', 'institution__nom')
