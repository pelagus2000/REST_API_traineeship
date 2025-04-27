from django.db import models


class Tourist(models.Model):
    TOURISM_CHOICES = [
        ('walking', 'пешком'),
        ('skiing', 'лыжи'),
        ('catamaran', 'катамаран'),
        ('kayak', 'байдарка'),
        ('ferry', 'пaром'),
        ('rafting', 'сплав'),
        ('cycling', 'велосипед'),
        ('auto', 'автомобиль'),
        ('moto', 'мотоцикл'),
        ('sail', 'парус'),
        ('horseback', 'верхом'),
    ]

    email = models.EmailField(max_length=255, verbose_name='Электронная почта')
    fam = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    otc = models.CharField(max_length=255, verbose_name='Отчество')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    type = models.CharField(max_length=20, choices=TOURISM_CHOICES, default='auto', verbose_name='Вид туризма')

    def __str__(self):
        return f"{self.fam} {self.name} {self.otc}"

    class Meta:
        verbose_name = 'Турист'
        verbose_name_plural = 'Туристы'