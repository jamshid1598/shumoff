from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True, verbose_name='Категория:')
    image = ImageField(upload_to="category/%Y/%m/%d/", verbose_name='Категория Образ:')

    primary   = models.BooleanField(default=True, verbose_name="Основная")
    tools     = models.BooleanField(default=False, verbose_name="инструменты")
    accessory = models.BooleanField(default=False, verbose_name="Аксессуар")
    
    class Meta:
        ordering            = ['category_name']
        verbose_name        = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url  

class Product(models.Model):
    image       = ImageField(upload_to="product/%Y/%m/%d/", verbose_name='Образ:')
    caption     = models.CharField(max_length=300, blank=True, null=True, verbose_name='Заголовок:')

    name        = models.CharField(max_length=300, verbose_name='название:')
    slug        = models.SlugField(max_length=320)

    description = models.TextField(verbose_name='Описание:')
    quantity    = models.PositiveIntegerField(default=0, verbose_name='Количество:')

    class CurrecyChoice(models.TextChoices):
        SUM="сумма",_('сум')
        USD='$',_('доллар')
        RUB='ruble',_('рубль')
        __empty__=_('')

    currency     = models.CharField( verbose_name='Тип валюты:', max_length=5, choices=CurrecyChoice.choices, default=CurrecyChoice.SUM,)
    price        = models.DecimalField( verbose_name='Цена', max_digits=10, decimal_places=2, default=100, validators=( MinValueValidator(1), MaxValueValidator(100000000),))
    discount     = models.DecimalField( verbose_name='Скидка Цена', max_digits=10, decimal_places=2, blank=True, null=True, validators=( MinValueValidator(1), MaxValueValidator(100000000),))

    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category', verbose_name='Категория:')
    digital      = models.BooleanField(default=False,null=True, blank=True)

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ['name', 'published_at', 'updated_at']
        verbose_name        = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('Core:detail-view', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def is_updated(self):
        if self.published_at == self.updated_at:
            return self.published_at
        else:
            self.updated_at
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Images(models.Model):
    model   = models.ForeignKey(Product,  on_delete=models.CASCADE, related_name="product_images",)
    images  = ImageField(upload_to='product-images/%Y/%m/%d/')
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name='Заголовок:')
    
    class Meta:
        verbose_name_plural = "Изображений: "

    def __str__(self):
        return self.model.name

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url   
