# tourist/admin.py
from django.contrib import admin
from .models import Tourist


class TouristAdmin(admin.ModelAdmin):
    list_display = ('id', 'fam', 'name', 'otc', 'email', 'phone')
    search_fields = ('email', 'fam', 'name', 'phone')


admin.site.register(Tourist, TouristAdmin)

