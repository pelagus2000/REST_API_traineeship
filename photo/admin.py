# photo/admin.py
from django.contrib import admin
from .models import Image
from django.utils.safestring import mark_safe


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_photo_preview')
    search_fields = ('title',)

    def get_photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 50px; max-width: 100px;" />')
        return "-"

    get_photo_preview.short_description = 'Предпросмотр'


admin.site.register(Image, ImageAdmin)