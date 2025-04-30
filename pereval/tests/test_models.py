# pereval/tests/test_models.py
from django.test import TestCase
from pereval.models import Pereval, TermsAgreement, ModerationComment, Notification
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image
import uuid


class PerevalModelTest(TestCase):
    """Тесты для модели Pereval"""

    def setUp(self):
        # Создаем необходимые связанные объекты
        self.tourist = Tourist.objects.create(
            email='test@example.com',
            fam='Тестов',
            name='Тест',
            otc='Тестович',
            phone='+7 999 999 9999'
        )

        self.coords = Coords.objects.create(
            latitude='45.3842',
            longitude='7.1525',
            height='1200'
        )

        self.image = Image.objects.create(
            photo='photo:image/png;base64,iVBORw0KGgoAAA==',
            title='Тестовое изображение'
        )

        # Создаем перевал для тестов
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

    def test_pereval_creation(self):
        """Тест создания перевала"""
        self.assertEqual(self.pereval.title, 'Тестовый')
        self.assertEqual(self.pereval.status, 'new')
        self.assertEqual(self.pereval.area, 'Altay')
        self.assertEqual(self.pereval.tourist, self.tourist)
        self.assertEqual(self.pereval.coords, self.coords)
        self.assertEqual(self.pereval.photo, self.image)

    def test_pereval_str_method(self):
        """Тест строкового представления перевала"""
        self.assertEqual(str(self.pereval), 'пер.  Тестовый')


class TermsAgreementModelTest(TestCase):
    """Тесты для модели TermsAgreement"""

    def setUp(self):
        self.token = str(uuid.uuid4())
        self.agreement = TermsAgreement.objects.create(
            token=self.token,
            is_valid=True
        )

    def test_terms_agreement_creation(self):
        """Тест создания объекта согласия с условиями"""
        self.assertEqual(self.agreement.token, self.token)
        self.assertTrue(self.agreement.is_valid)

    def test_terms_agreement_str_method(self):
        """Тест строкового представления согласия с условиями"""
        self.assertEqual(str(self.agreement), f"{self.token} - Активен")

        # Изменяем статус и проверяем строковое представление
        self.agreement.is_valid = False
        self.agreement.save()
        self.assertEqual(str(self.agreement), f"{self.token} - Использован")


class NotificationModelTest(TestCase):
    """Тесты для модели Notification"""

    def setUp(self):
        # Создаем необходимые связанные объекты
        self.tourist = Tourist.objects.create(
            email='test@example.com',
            fam='Тестов',
            name='Тест',
            otc='Тестович',
            phone='+7 999 999 9999'
        )

        self.coords = Coords.objects.create(
            latitude='45.3842',
            longitude='7.1525',
            height='1200'
        )

        self.image = Image.objects.create(
            photo='photo:image/png;base64,iVBORw0KGgoAAA==',
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

        # Создаем уведомление
        self.notification = Notification.objects.create(
            pereval=self.pereval,
            notification_type='status_change',
            message='Статус вашего перевала изменен на Принят.',
            is_sent=False
        )

    def test_notification_creation(self):
        """Тест создания уведомления"""
        self.assertEqual(self.notification.pereval, self.pereval)
        self.assertEqual(self.notification.notification_type, 'status_change')
        self.assertEqual(self.notification.message, 'Статус вашего перевала изменен на Принят.')
        self.assertFalse(self.notification.is_sent)

    def test_notification_ordering(self):
        """Тест порядка сортировки уведомлений"""
        # Создаем еще одно уведомление
        new_notification = Notification.objects.create(
            pereval=self.pereval,
            notification_type='comment',
            message='Новый комментарий к вашему перевалу.',
            is_sent=False
        )

        # Проверяем, что новое уведомление будет первым в списке (обратный порядок по времени создания)
        self.assertEqual(list(Notification.objects.all())[0], new_notification)