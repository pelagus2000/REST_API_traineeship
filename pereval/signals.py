# pereval/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pereval, ModerationComment, Notification


@receiver(post_save, sender=Pereval)
def create_status_notification(sender, instance, created, **kwargs):
    # Обработка случая, когда update_fields равен None
    update_fields = kwargs.get('update_fields')

    # Если объект не новый и либо update_fields is None, либо 'status' в update_fields
    if not created and (update_fields is None or 'status' in update_fields):
        status_display = instance.get_status_display()
        Notification.objects.create(
            pereval=instance,
            notification_type='status_change',
            message=f'Статус вашего перевала "{instance.title}" изменен на "{status_display}".'
        )


@receiver(post_save, sender=ModerationComment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            pereval=instance.pereval,
            notification_type='comment',
            message=f'Модератор оставил комментарий к вашему перевалу "{instance.pereval.title}".'
        )
