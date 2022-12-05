from django.db import models


class Category(models.Model):
    """Модель для создания категории."""
    name = models.CharField(max_length=120, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Ad(models.Model):
    """Модель для создания объявления."""
    title = models.CharField(max_length=120, unique=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='Цена')
    city = models.CharField(max_length=60, unique=True, verbose_name='Город')
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name='ads',
        verbose_name='Категория',
    )
    thumbnail_link = models.URLField(max_length=200, verbose_name='Миниатюра')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    author = models.CharField(max_length=40, blank=True, verbose_name='Автор')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Image(models.Model):
    """Модель для создания изображения объявления."""
    image_link = models.URLField(max_length=200, verbose_name='Изображение')
    ad = models.ForeignKey(to=Ad, on_delete=models.CASCADE, related_name='images', verbose_name='Объявление')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.image_link
