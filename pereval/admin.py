# pereval/admin.py
from django.contrib import admin
from .models import Pereval, TermsAgreement, ModerationComment

from coordinates.models import Coords
from photo.models import Image
from tourist.models import Tourist

class ModerationCommentInline(admin.TabularInline):
    model = ModerationComment
    extra = 1
    fields = ('text', 'moderator')
    readonly_fields = ('created',)

    def save_model(self, request, obj, form, change):
        if not obj.moderator:
            obj.moderator = request.user
        super().save_model(request, obj, form, change)

class PerevalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'beauty_title', 'tourist_email', 'status', 'created')
    list_filter = ('status', 'area', 'level', 'created')
    search_fields = ('title', 'beauty_title', 'tourist__email', 'tourist__fam', 'tourist__name')
    readonly_fields = ('created',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'beauty_title', 'other_titles', 'connect', 'level', 'area')
        }),
        ('Статус модерации', {
            'fields': ('status',)
        }),
        ('Связанные объекты', {
            'fields': ('tourist', 'coords', 'photo')
        }),
        ('Метаданные', {
            'fields': ('created',)
        }),
    )

    def tourist_email(self, obj):
        return obj.tourist.email

    tourist_email.admin_order_field = 'tourist__email'
    tourist_email.short_description = 'Email туриста'


    actions = ['mark_as_pending', 'mark_as_accepted', 'mark_as_rejected']

    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} перевалов взяты в работу.')

    mark_as_pending.short_description = "Взять в работу выбранные перевалы"

    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} перевалов успешно приняты.')

    mark_as_accepted.short_description = "Принять выбранные перевалы"

    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} перевалов отклонены.')

    mark_as_rejected.short_description = "Отклонить выбранные перевалы"
    inlines = [ModerationCommentInline]


admin.site.register(Pereval, PerevalAdmin)
admin.site.register(TermsAgreement)