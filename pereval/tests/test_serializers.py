
# pereval/tests/test_serializers.py
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from pereval.models import Pereval, TermsAgreement, Notification
from pereval.serializers import (
    PerevalSerializer,
    PerevalUpdateSerializer,
    PerevalDetailSerializer,
    PerevalListSerializer,
    ModerationSerializer,
    NotificationSerializer
)
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile


class PerevalSerializerTest(TestCase):
    """Тесты для сериализатора PerevalSerializer"""

    def setUp(self):
        # Создаем токен для условий соглашения
        self.token = str(uuid.uuid4())
        self.terms_agreement = TermsAgreement.objects.create(
            token=self.token,
            is_valid=True
        )

        # Создаем тестовое изображение
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00',
            content_type='image/jpeg'
        )

        # Подготавливаем данные для сериализатора
        self.pereval_data = {
            'beauty_title': 'пер. ',
            'title': 'Тестовый',
            'other_titles': 'Альтернативный',
            'connect': 'Соединяет что-то',
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
                'latitude': 45.3842,  # Числовое значение вместо строки
                'longitude': 7.1525,  # Числовое значение вместо строки
                'height': 1200  # Числовое значение вместо строки
            },
            'photo': {
                'photo': self.test_image,  # Используем объект файла вместо base64
                'title': 'Тестовое изображение'
            },
            'terms_token': self.token
        }

    def test_pereval_serializer_valid_data(self):
        """Проверка сериализатора с корректными данными"""
        serializer = PerevalSerializer(data=self.pereval_data)
        # Если валидация не проходит, выведем ошибки для отладки
        if not serializer.is_valid():
            print(f"Ошибки валидации: {serializer.errors}")
        self.assertTrue(serializer.is_valid())

    def test_pereval_serializer_missing_title(self):
        """Проверка сериализатора с отсутствующим обязательным полем"""
        data = self.pereval_data.copy()
        data.pop('title')
        serializer = PerevalSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_pereval_serializer_invalid_terms_token(self):
        """Проверка валидации токена соглашения"""
        # Проверка с несуществующим токеном
        data = self.pereval_data.copy()
        data['terms_token'] = 'invalid_token'
        serializer = PerevalSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('terms_token', serializer.errors)

        # Проверка с недействительным токеном
        self.terms_agreement.is_valid = False
        self.terms_agreement.save()

        serializer = PerevalSerializer(data=self.pereval_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('terms_token', serializer.errors)


class ModerationSerializerTest(TestCase):
    """Тесты для сериализатора ModerationSerializer"""

    def test_moderation_serializer_valid_status(self):
        """Проверка сериализатора с допустимыми статусами"""
        valid_statuses = ['new', 'pending', 'accepted', 'rejected']

        for status in valid_statuses:
            serializer = ModerationSerializer(data={'status': status})
            self.assertTrue(serializer.is_valid())

    def test_moderation_serializer_invalid_status(self):
        """Проверка сериализатора с недопустимым статусом"""
        serializer = ModerationSerializer(data={'status': 'invalid_status'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)