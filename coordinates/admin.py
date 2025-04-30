# coordinates/admin.py
from django.contrib import admin
from .models import Coords

class CoordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'height')
    search_fields = ('latitude', 'longitude', 'height')

admin.site.register(Coords, CoordsAdmin)