from django.db import models



class Image(models.Model):
    photo = models.ImageField(upload_to='pereval_images/', verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Название')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
