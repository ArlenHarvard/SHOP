from django.db import models
from django.db.models import ForeignKey
from .constants import NULLABLE

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='media/category_image', verbose_name='Изображение')
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Родительская категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        ancestors = []
        category = self
        while category:
            ancestors.append(category.title)
            category = category.parent_category
        return ' > '.join(reversed(ancestors))


class City(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

class District(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город', related_name='districts')

    def __str__(self):
        return self.title


class Image(models.Model):
    estate = models.ForeignKey('Estate', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/additional_image')

class Estate(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    cover = models.ImageField(upload_to='media/products_image', verbose_name='Обложка')
    area = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Площадь в метрах')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город')
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='Улица')
    geo = models.TextField(verbose_name='Геолокация')
    price = models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Цена')
    descriptions = models.TextField(verbose_name='Описание')
    video = models.FileField(upload_to='media/product_video', verbose_name='Видео')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимости'
