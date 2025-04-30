from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json
import uuid

from pereval.models import Pereval, TermsAgreement, Notification, ModerationComment
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image


class PerevalViewSetTest(TestCase):
    """Тесты для PerevalViewSet"""

    def setUp(self):
        self.client = APIClient()

        # Создаем туриста для тестов
        self.tourist = Tourist.objects.create(
            email='test@example.com',
            fam='Тестов',
            name='Тест',
            otc='Тестович',
            phone='+7 999 999 9999'
        )

        # Создаем координаты
        self.coords = Coords.objects.create(
            latitude='45.3842',
            longitude='7.1525',
            height='1200'
        )

        # Создаем изображение - исправлено поле data на photo
        self.image = Image.objects.create(
            photo='data:image/png;base64,iVBORw0KGgoAAA==',
            title='Тестовое изображение'
        )

        # Создаем перевал
        self.pereval = Pereval.objects.create(
            beauty_title='пер. ',
            title='Тестовый',
            other_titles='Альтернативный',
            connect='Соединяет что-то',
            level='summer',
            status='new',
            area='Altay',
            tourist=self.tourist,
            coords=self.coords,
            photo=self.image
        )

        # Создаем токен согласия
        self.token = str(uuid.uuid4())
        self.terms_agreement = TermsAgreement.objects.create(
            token=self.token,
            is_valid=True
        )

        # Данные для запроса на создание перевала
        self.pereval_data = {
            'beauty_title': 'пер. ',
            'title': 'Новый перевал',
            'other_titles': 'Другое название',
            'connect': 'Соединяет что-то новое',
            'level': 'summer',
            'area': 'Altay',
            'tourist': {
                'email': 'test@example.com',
                'fam': 'Тестов',
                'name': 'Тест',
                'otc': 'Тестович',
                'phone': '+7 999 999 9999'
            },
            'coords': {
                'latitude': '45.3842',
                'longitude': '7.1525',
                'height': '1200'
            },
            'photo': {
                'photo': 'data:image/png;base64,iVBORw0KGgoAAA==',
                'title': 'Тестовое изображение'
            },
            'terms_token': self.token
        }

    def test_filter_by_email(self):
        """Тест фильтрации перевалов по email туриста"""
        url = reverse('submitdata-list') + f'?user__email={self.tourist.email}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Тестовый')

    def test_partial_update_pereval(self):
        """Тест частичного обновления перевала (PATCH)"""
        url = reverse('submitdata-detail', kwargs={'pk': self.pereval.id})  # Используем kwargs для правильной передачи параметров


        update_data = {
            'title': 'Обновленное название',
            'beauty_title': 'пер. Новый'
        }

        response = self.client.patch(
            url,
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)

        # Перезагружаем объект и проверяем изменения
        self.pereval.refresh_from_db()
        self.assertEqual(self.pereval.title, 'Обновленное название')
        self.assertEqual(self.pereval.beauty_title, 'пер. Новый')

    def test_full_update_pereval(self):
        """Тест полного обновления перевала (PUT)"""
        url = reverse('submitdata-detail', kwargs={'pk': self.pereval.id})

        update_data = {
            'beauty_title': 'пер. Полное',
            'title': 'Полное обновление',
            'other_titles': 'Новое альтернативное',
            'connect': 'Новое соединение',
            'level': 'winter',
            'area': 'Pamiro-Alai'
        }

        response = self.client.put(
            url,
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)

        # Перезагружаем объект и проверяем изменения
        self.pereval.refresh_from_db()
        self.assertEqual(self.pereval.title, 'Полное обновление')
        self.assertEqual(self.pereval.beauty_title, 'пер. Полное')
        self.assertEqual(self.pereval.level, 'winter')



class NotificationTest(TestCase):
    """Тесты для системы уведомлений"""

    def setUp(self):
        # Создаем туриста для тестов
        self.tourist = Tourist.objects.create(
            email='test@example.com',
            fam='Тестов',
            name='Тест',
            otc='Тестович',
            phone='+7 999 999 9999'
        )

        # Создаем координаты
        self.coords = Coords.objects.create(
            latitude='45.3842',
            longitude='7.1525',
            height='1200'
        )

        # Создаем изображение
        self.image = Image.objects.create(
            photo='data:image/png;base64,iVBORw0KGgoAAA==',
            title='Тестовое изображение'
        )

        # Создаем перевал
        self.pereval = Pereval.objects.create(
            beauty_title='пер. ',
            title='Тестовый',
            other_titles='Альтернативный',
            connect='Соединяет что-то',
            level='summer',
            status='new',
            area='Altay',
            tourist=self.tourist,
            coords=self.coords,
            photo=self.image
        )

    def test_status_change_notification(self):
        """Тест создания уведомления при изменении статуса перевала"""
        # Проверяем начальное количество уведомлений
        self.assertEqual(Notification.objects.count(), 0)

        # Меняем статус перевала с явным указанием update_fields
        # Это должно создать уведомление через сигнал
        self.pereval.status = 'accepted'
        self.pereval.save(update_fields=['status'])

        # Проверяем, что создано уведомление
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.first()
        self.assertEqual(notification.pereval, self.pereval)
        self.assertEqual(notification.notification_type, 'status_change')
        self.assertIn('изменен на "Принят"', notification.message)

    def test_status_change_notification_without_update_fields(self):
        """Тест создания уведомления при изменении статуса перевала без указания update_fields"""
        # Проверяем начальное количество уведомлений
        self.assertEqual(Notification.objects.count(), 0)

        # Меняем статус перевала без указания update_fields
        # С обновленным сигналом, это также должно создать уведомление
        self.pereval.status = 'accepted'
        self.pereval.save()

        # Проверяем, что создано уведомление
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.first()
        self.assertEqual(notification.pereval, self.pereval)
        self.assertEqual(notification.notification_type, 'status_change')
        self.assertIn('изменен на "Принят"', notification.message)

    def test_comment_notification(self):
        """Тест создания уведомления при добавлении комментария модератора"""
        # Проверяем начальное количество уведомлений
        self.assertEqual(Notification.objects.count(), 0)

        # Создаем комментарий модератора
        ModerationComment.objects.create(
            pereval=self.pereval,
            text='Тестовый комментарий модератора',
            moderator='Тестовый модератор'
        )

        # Проверяем, что создано уведомление
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.first()
        self.assertEqual(notification.pereval, self.pereval)
        self.assertEqual(notification.notification_type, 'comment')
        self.assertIn('Модератор оставил комментарий', notification.message)