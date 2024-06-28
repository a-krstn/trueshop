from django.db import models


class Category(models.Model):
    """Модель категории продукта"""

    name = models.CharField(max_length=100,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=150,
                            unique=True,
                            verbose_name='Слаг категории')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')
    name = models.CharField(max_length=200,
                            verbose_name='Продукт')
    slug = models.SlugField(max_length=250,
                            verbose_name='Слаг продукта')
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True,
                              verbose_name='Изображение продукта')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена')
    available = models.BooleanField(default=True,
                                    verbose_name='Наличие товара')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Обновлен')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
