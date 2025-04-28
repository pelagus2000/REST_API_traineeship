from django.db import models

from coordinates.models import Coords
from photo.models import Image
from tourist.models import Tourist


class Pereval(models.Model):
    AREA_CHOICES = [
        ('Planet Earth', 'Планета Земля'),
        ('Pamiro-Alai', 'Памиро-Алай'),
        ('Altay', 'Алтай'),
        ('Nothern-Chuiskiy Ridge', 'Северо-Чуйский хребет'),
        ('Southern-Chuiskiy Ridge', 'Южно-Чуйский хребет'),
        ('Katun Ridge', 'Катунский хребет'),
        ('Fansky mountains', 'Фанские горы'),
        ('Gussarskiy Ridge(west from The Anzob Pass)', 'Гиссарский хребет (участок западнее перевала Анзоб)'),
        ('Matchinskiy mountain knot', 'Матчинский горный узел'),
        ('Takali mountain knot-Turkestan ridge', 'Горный узел Такали-Туркестанский хребет'),
        ('High Alay', 'Высокий Алай'),
        ('Kichik-Alay and Eastern Alay', 'Кичик-Алай и Восточный Алай'),
        ('Aladaglar', 'Аладаглар'),
        ('Tavr', 'Тавр'),
        ('Sayan mountains', 'Саяны'),
        ('Listvyaga Ridge', 'Хребет Листвяга'),
        ('Ivanovsky Ridge', 'Ивановский хребет'),
        ('Mungun-Taiga massif', 'Массив Мунгун-Тайга'),
        ('Tsagan-Shibetu Ridge', 'Хребет Цаган-Шибэту'),
        ('Chikhachev Ridge (Sailugem)', 'Хребет Чихачева (Сайлюгем)'),
        ('Shapshalsky Ridge', 'Шапшальский хребет'),
        ('Southern Altai Ridge', 'Хребет Южный Алтай'),
        ('Mongolian Altai Ridge', 'Хребет Монгольский Алтай'),
        ('Western Sayan', 'Западный Саян'),
        ('Eastern Sayan', 'Восточный Саян'),
        ('Kuznetsky Alatau', 'Кузнецкий Алатау'),
        ('Kurai ridge', 'Курайский хребет')
    ]


    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('pending', 'В работе'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    ]

    LEVEL_CHOICES = [
        ('winter', 'Зима'),
        ('summer', 'Лето'),
        ('autumn', 'Осень'),
        ('spring', 'Весна'),
    ]

    beauty_title = models.CharField(max_length=255, verbose_name='Сокращенное название', blank=True)
    title = models.CharField(max_length=255, verbose_name='Полное название')
    other_titles = models.CharField(max_length=255, verbose_name='Альтернативное название', blank=True)
    connect = models.CharField(max_length=255, verbose_name='Соединяет', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='summer',
                                 verbose_name='Уровень сложности')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    area = models.CharField(max_length=100, choices=AREA_CHOICES, default='Planet Earth', verbose_name='Область')
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, related_name='tourist',verbose_name='Турист')
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE, related_name='coordinates', verbose_name='Координаты')
    photo = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image')


    def __str__(self):
        return f"{self.beauty_title} {self.title}"

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'


class TermsAgreement(models.Model):
    token = models.CharField(max_length=100, unique=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token} - {'Активен' if self.is_valid else 'Использован'}"

    class Meta:
        verbose_name = 'Согласие с условиями'
        verbose_name_plural = 'Согласия с условиями'
